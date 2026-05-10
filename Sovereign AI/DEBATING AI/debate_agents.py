import os
from typing import List, Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
import json
from mcp_server import mcp_server

class DebateState(TypedDict):
    topic: str
    agent1_position: str
    agent2_position: str
    agent1_arguments: Annotated[List, add_messages]
    agent2_arguments: Annotated[List, add_messages]
    current_round: int
    max_rounds: int
    winner: str
    reasoning: str

class DebateAgent:
    def __init__(self, name: str, position: str, llm: ChatOllama):
        self.name = name
        self.position = position
        self.llm = llm
        self.session_id = None
    
    def set_session(self, session_id: str):
        """Set the MCP session ID for context management"""
        self.session_id = session_id
    
    def generate_argument(self, topic: str, opponent_arguments: List[str], round_num: int) -> str:
        """Generate an argument based on position and opponent's previous arguments"""
        
        # Get relevant context from MCP
        context_data = {}
        if self.session_id:
            context_data = mcp_server.get_relevant_context(self.session_id, self.name, round_num)
        
        position_prompt = {
            "FOR": f"You are arguing FOR the topic: '{topic}'. Provide strong, compelling arguments supporting this position.",
            "AGAINST": f"You are arguing AGAINST the topic: '{topic}'. Provide strong, compelling arguments opposing this position.",
            "NEUTRAL": f"You are taking a NEUTRAL stance on the topic: '{topic}'. Provide balanced arguments considering both sides."
        }
        
        # Build context-aware prompt
        context_info = ""
        if context_data:
            context_info = f"""

Debate Context:
- Topic Analysis: {context_data.get('topic_analysis', {})}
- Progress: {context_data.get('debate_progress', 'Unknown')}
- Your Position: {context_data.get('agent_position', self.position)}
- Opponent Position: {context_data.get('opponent_position', 'Unknown')}
"""
        
        opponent_context = ""
        if opponent_arguments:
            opponent_context = f"\n\nYour opponent's recent arguments:\n" + "\n".join([f"- {arg}" for arg in opponent_arguments[-2:]])
            opponent_context += "\n\nAddress or counter these points in your argument."
        
        prompt = f"""
{position_prompt[self.position]}

This is Round {round_num}. Make your argument impactful and persuasive.{context_info}{opponent_context}

Guidelines:
1. Be specific and provide concrete examples
2. Use logical reasoning and evidence
3. Address opponent's points when relevant
4. Maintain your assigned position consistently
5. Keep your argument concise but powerful (100-150 words)
6. Use rhetorical devices to make your point stronger
7. Consider the topic type and complexity in your approach

Your argument:
"""
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        # Clean up the response
        argument = response.content.strip()
        
        # Remove any JSON formatting or system messages
        if argument.startswith('{') or argument.startswith('['):
            try:
                parsed = json.loads(argument)
                if isinstance(parsed, dict) and 'argument' in parsed:
                    argument = parsed['argument']
            except:
                pass
        
        # Ensure we have a substantial argument
        if len(argument) < 50:
            argument = f"Based on my position as {self.position}, I believe that {topic} {'should be supported' if self.position == 'FOR' else 'should be opposed' if self.position == 'AGAINST' else 'requires careful consideration of both sides'}. This stance is supported by strong evidence and logical reasoning."
        
        # Store argument in MCP
        if self.session_id:
            mcp_server.add_argument(self.session_id, self.name, argument)
        
        return argument

class JudgeAgent:
    def __init__(self, llm: ChatOllama):
        self.llm = llm
    
    def _extract_argument_points(self, arguments: List[str], agent_name: str) -> Dict[str, Any]:
        """Extract and categorize specific points from agent arguments"""
        points_analysis = {
            "evidence_points": [],
            "logic_points": [],
            "counter_points": [],
            "persuasion_points": [],
            "consistency_points": [],
            "total_strength": 0,
            "specific_claims": [],
            "examples_used": [],
            "reasoning_chains": []
        }
        
        for i, arg in enumerate(arguments):
            arg_lower = arg.lower()
            
            # Extract specific claims and statements
            sentences = arg.split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20:  # Only meaningful sentences
                    # Extract evidence-based points with specific content
                    if any(word in sentence.lower() for word in ["evidence", "example", "fact", "data", "statistic", "study", "research", "shows", "demonstrates", "proves"]):
                        points_analysis["evidence_points"].append(f"Round {i+1}: {sentence}")
                        points_analysis["examples_used"].append(sentence)
                        points_analysis["total_strength"] += 3
                    
                    # Extract logical reasoning with actual content
                    elif any(word in sentence.lower() for word in ["because", "therefore", "thus", "consequently", "leads to", "results in", "means that", "implies"]):
                        points_analysis["logic_points"].append(f"Round {i+1}: {sentence}")
                        points_analysis["reasoning_chains"].append(sentence)
                        points_analysis["total_strength"] += 2
                    
                    # Extract counter-arguments with specific content
                    elif any(word in sentence.lower() for word in ["however", "but", "although", "whereas", "counter", "oppose", "refute", "contradict"]):
                        points_analysis["counter_points"].append(f"Round {i+1}: {sentence}")
                        points_analysis["total_strength"] += 3
                    
                    # Extract specific claims
                    elif any(word in sentence.lower() for word in ["believe", "argue", "contend", "maintain", "assert", "propose"]):
                        points_analysis["specific_claims"].append(f"Round {i+1}: {sentence}")
                        points_analysis["total_strength"] += 1
                    
                    # Extract persuasive language
                    elif any(word in sentence.lower() for word in ["clearly", "obviously", "undeniable", "certainly", "crucial", "essential", "critical", "important"]):
                        points_analysis["persuasion_points"].append(f"Round {i+1}: {sentence}")
                        points_analysis["total_strength"] += 1
        
        return points_analysis
    
    def _extract_relevant_phrase(self, argument: str, keywords: List[str]) -> str:
        """Extract the most relevant phrase containing the keyword"""
        sentences = argument.split('.')
        best_sentence = ""
        best_score = 0
        
        for sentence in sentences:
            score = sum(1 for keyword in keywords if keyword.lower() in sentence.lower())
            if score > best_score and len(sentence.strip()) > 10:
                best_score = score
                best_sentence = sentence.strip()
        
        return best_sentence if best_sentence else argument[:100] + "..." if len(argument) > 100 else argument
    
    def evaluate_debate(self, topic: str, agent1_position: str, agent2_position: str, 
                       agent1_args: List[str], agent2_args: List[str]) -> Dict[str, str]:
        """Evaluate the debate and declare a winner based on actual argument points"""
        
        # Ensure we have arguments to evaluate
        if not agent1_args or not agent2_args:
            return {
                "winner": "Tie",
                "reasoning": "Insufficient arguments to make a proper judgment.",
                "agent1_score": "5",
                "agent2_score": "5"
            }
        
        # Extract and analyze points from both agents
        agent1_points = self._extract_argument_points(agent1_args, "Agent 1")
        agent2_points = self._extract_argument_points(agent2_args, "Agent 2")
        
        # Calculate detailed scores
        agent1_total = agent1_points["total_strength"]
        agent2_total = agent2_points["total_strength"]
        
        # Normalize scores to 10-point scale
        max_possible = max(len(agent1_args), len(agent2_args)) * 10  # Max possible points per argument
        agent1_score = min(10, max(1, round((agent1_total / max_possible) * 10)))
        agent2_score = min(10, max(1, round((agent2_total / max_possible) * 10)))
        
        # Determine winner based on actual points
        if agent1_total > agent2_total:
            winner = "Agent 1"
            winning_points = agent1_points
            winning_score = agent1_score
            losing_score = agent2_score
        elif agent2_total > agent1_total:
            winner = "Agent 2"
            winning_points = agent2_points
            winning_score = agent2_score
            losing_score = agent1_score
        else:
            # If points are tied, use quality over quantity
            agent1_quality = len(agent1_points["evidence_points"]) + len(agent1_points["counter_points"])
            agent2_quality = len(agent2_points["evidence_points"]) + len(agent2_points["counter_points"])
            
            if agent1_quality > agent2_quality:
                winner = "Agent 1"
                winning_points = agent1_points
                winning_score = agent1_score
                losing_score = agent2_score
            elif agent2_quality > agent1_quality:
                winner = "Agent 2"
                winning_points = agent2_points
                winning_score = agent2_score
                losing_score = agent1_score
            else:
                # Final tie-breaker: number of logical reasoning points
                agent1_logic = len(agent1_points["logic_points"])
                agent2_logic = len(agent2_points["logic_points"])
                
                if agent1_logic >= agent2_logic:
                    winner = "Agent 1"
                    winning_points = agent1_points
                    winning_score = agent1_score
                    losing_score = agent2_score
                else:
                    winner = "Agent 2"
                    winning_points = agent2_points
                    winning_score = agent2_score
                    losing_score = agent1_score
        
        # Generate detailed reasoning based on ACTUAL extracted points
        reasoning_parts = []
        
        # Use specific evidence examples
        if winning_points["examples_used"]:
            example = winning_points["examples_used"][0]
            if len(example) > 100:
                example = example[:100] + "..."
            reasoning_parts.append(f"provided compelling evidence: '{example}'")
        
        # Use specific reasoning chains
        if winning_points["reasoning_chains"]:
            reasoning_chain = winning_points["reasoning_chains"][0]
            if len(reasoning_chain) > 80:
                reasoning_chain = reasoning_chain[:80] + "..."
            reasoning_parts.append(f"demonstrated logical reasoning: '{reasoning_chain}'")
        
        # Use specific counter-arguments
        if winning_points["counter_points"]:
            counter = winning_points["counter_points"][0]
            # Extract just the counter part
            if ":" in counter:
                counter = counter.split(":", 1)[1].strip()
            if len(counter) > 80:
                counter = counter[:80] + "..."
            reasoning_parts.append(f"effectively countered with: '{counter}'")
        
        # Use specific claims if no other strong points
        if not reasoning_parts and winning_points["specific_claims"]:
            claim = winning_points["specific_claims"][0]
            if ":" in claim:
                claim = claim.split(":", 1)[1].strip()
            if len(claim) > 80:
                claim = claim[:80] + "..."
            reasoning_parts.append(f"made strong argument: '{claim}'")
        
        # Build final reasoning with specific content
        if reasoning_parts:
            reasoning = f"{winner} wins by {', '.join(reasoning_parts[:2])}, scoring {winning_score}/10 against {losing_score}/10."
        else:
            # Fallback with actual argument content
            if agent1_args if winner == "Agent 1" else agent2_args:
                best_arg = (agent1_args if winner == "Agent 1" else agent2_args)[0]
                if len(best_arg) > 100:
                    best_arg = best_arg[:100] + "..."
                reasoning = f"{winner} wins with superior argumentation: '{best_arg}', scoring {winning_score}/10."
            else:
                reasoning = f"{winner} wins with stronger argument structure, scoring {winning_score}/10."
        
        # Compile key winning points with ACTUAL content
        key_points = []
        
        # Add actual examples used
        if winning_points["examples_used"]:
            key_points.extend(winning_points["examples_used"][:2])
        
        # Add actual reasoning chains
        if winning_points["reasoning_chains"]:
            key_points.extend(winning_points["reasoning_chains"][:1])
        
        # Add actual counter-arguments
        if winning_points["counter_points"]:
            key_points.extend(winning_points["counter_points"][:1])
        
        # Format key points for display
        if key_points:
            # Clean up key points for display
            clean_points = []
            for point in key_points[:3]:
                if ":" in point:
                    point = point.split(":", 1)[1].strip()
                if len(point) > 120:
                    point = point[:120] + "..."
                clean_points.append(point)
            key_points_text = "; ".join(clean_points)
        else:
            key_points_text = "Strong argumentation with specific evidence and reasoning"
        
        return {
            "winner": winner,
            "reasoning": reasoning,
            "agent1_score": str(agent1_score),
            "agent2_score": str(agent2_score),
            "key_points": key_points_text,
            "agent1_points": agent1_points,
            "agent2_points": agent2_points
        }

class DebateOrchestrator:
    def __init__(self, model_name: str = "llama3.2:1b"):
        self.llm = ChatOllama(
            model=model_name,
            temperature=0.7,
            base_url="http://localhost:11434"
        )
        self.current_session_id = None
    
    def create_debate_session(self, topic: str, agent1_position: str, agent2_position: str, 
                             max_rounds: int = 3) -> str:
        """Create a new debate session using MCP"""
        self.current_session_id = mcp_server.create_context(
            topic=topic,
            agent1_position=agent1_position,
            agent2_position=agent2_position,
            max_rounds=max_rounds
        )
        return self.current_session_id
        
    def create_debate_graph(self) -> StateGraph:
        """Create the debate workflow using LangGraph"""
        
        workflow = StateGraph(DebateState)
        
        # Add nodes
        workflow.add_node("agent1_turn", self.agent1_turn)
        workflow.add_node("agent2_turn", self.agent2_turn)
        workflow.add_node("check_rounds", self.check_rounds)
        workflow.add_node("judge_debate", self.judge_debate)
        
        # Add edges
        workflow.set_entry_point("agent1_turn")
        workflow.add_edge("agent1_turn", "agent2_turn")
        workflow.add_edge("agent2_turn", "check_rounds")
        workflow.add_conditional_edges(
            "check_rounds",
            self.should_continue,
            {
                "continue": "agent1_turn",
                "judge": "judge_debate"
            }
        )
        workflow.add_edge("judge_debate", END)
        
        return workflow.compile()
    
    def agent1_turn(self, state: DebateState) -> DebateState:
        """Agent 1's turn to argue"""
        agent1 = DebateAgent("Agent 1", state["agent1_position"], self.llm)
        agent1.set_session(self.current_session_id)
        
        opponent_args = [arg.content if hasattr(arg, 'content') else str(arg) 
                        for arg in state["agent2_arguments"]]
        
        argument = agent1.generate_argument(
            state["topic"], 
            opponent_args, 
            state["current_round"]
        )
        
        state["agent1_arguments"].append(HumanMessage(content=argument))
        return state
    
    def agent2_turn(self, state: DebateState) -> DebateState:
        """Agent 2's turn to argue"""
        agent2 = DebateAgent("Agent 2", state["agent2_position"], self.llm)
        agent2.set_session(self.current_session_id)
        
        opponent_args = [arg.content if hasattr(arg, 'content') else str(arg) 
                        for arg in state["agent1_arguments"]]
        
        argument = agent2.generate_argument(
            state["topic"], 
            opponent_args, 
            state["current_round"]
        )
        
        state["agent2_arguments"].append(HumanMessage(content=argument))
        return state
    
    def check_rounds(self, state: DebateState) -> DebateState:
        """Check if debate should continue or go to judging"""
        state["current_round"] += 1
        return state
    
    def should_continue(self, state: DebateState) -> str:
        """Determine if debate should continue"""
        if state["current_round"] >= state["max_rounds"]:
            return "judge"
        return "continue"
    
    def judge_debate(self, state: DebateState) -> DebateState:
        """Judge the debate and determine winner"""
        judge = JudgeAgent(self.llm)
        
        agent1_args = [arg.content if hasattr(arg, 'content') else str(arg) 
                      for arg in state["agent1_arguments"]]
        agent2_args = [arg.content if hasattr(arg, 'content') else str(arg) 
                      for arg in state["agent2_arguments"]]
        
        result = judge.evaluate_debate(
            state["topic"],
            state["agent1_position"],
            state["agent2_position"],
            agent1_args,
            agent2_args
        )
        
        state["winner"] = result.get("winner", "Tie")
        state["reasoning"] = result.get("reasoning", "No reasoning provided")
        
        # Store detailed points analysis in the state for later access
        state["agent1_points"] = result.get("agent1_points", {})
        state["agent2_points"] = result.get("agent2_points", {})
        state["agent1_score"] = result.get("agent1_score", "5")
        state["agent2_score"] = result.get("agent2_score", "5")
        state["key_points"] = result.get("key_points", "")
        
        # Conclude debate in MCP
        if self.current_session_id:
            mcp_server.conclude_debate(
                self.current_session_id,
                state["winner"],
                state["reasoning"]
            )
        
        return state
    
    def run_debate(self, topic: str, agent1_position: str, agent2_position: str, 
                   max_rounds: int = 3) -> Dict[str, Any]:
        """Run a complete debate with MCP integration"""
        
        # Create MCP session
        session_id = self.create_debate_session(topic, agent1_position, agent2_position, max_rounds)
        
        initial_state = DebateState(
            topic=topic,
            agent1_position=agent1_position,
            agent2_position=agent2_position,
            agent1_arguments=[],
            agent2_arguments=[],
            current_round=1,
            max_rounds=max_rounds,
            winner="",
            reasoning=""
        )
        
        graph = self.create_debate_graph()
        final_state = graph.invoke(initial_state)
        
        # Convert arguments to readable format
        agent1_args = [arg.content if hasattr(arg, 'content') else str(arg) 
                      for arg in final_state["agent1_arguments"]]
        agent2_args = [arg.content if hasattr(arg, 'content') else str(arg) 
                      for arg in final_state["agent2_arguments"]]
        
        # Get MCP context for additional data
        mcp_context = mcp_server.get_context(session_id)
        
        return {
            "session_id": session_id,
            "topic": final_state["topic"],
            "agent1_position": final_state["agent1_position"],
            "agent2_position": final_state["agent2_position"],
            "agent1_arguments": agent1_args,
            "agent2_arguments": agent2_args,
            "winner": final_state["winner"],
            "reasoning": final_state["reasoning"],
            "rounds": final_state["current_round"] - 1,
            "agent1_score": final_state.get("agent1_score", "5"),
            "agent2_score": final_state.get("agent2_score", "5"),
            "key_points": final_state.get("key_points", ""),
            "agent1_points": final_state.get("agent1_points", {}),
            "agent2_points": final_state.get("agent2_points", {}),
            "mcp_context": mcp_server.export_context(session_id) if mcp_context else None,
            "global_stats": mcp_server.get_global_stats()
        }
