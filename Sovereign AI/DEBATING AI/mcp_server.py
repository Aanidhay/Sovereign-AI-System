"""
Model Context Protocol (MCP) Server for AI Debate Arena
Provides context management and storage for debate sessions
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

@dataclass
class DebateContext:
    """Context data structure for debate sessions"""
    session_id: str
    topic: str
    agent1_position: str
    agent2_position: str
    agent1_arguments: List[str]
    agent2_arguments: List[str]
    current_round: int
    max_rounds: int
    timestamp: str
    metadata: Dict[str, Any]

class MCPServer:
    """Model Context Protocol Server for managing debate context"""
    
    def __init__(self):
        self.contexts: Dict[str, DebateContext] = {}
        self.global_context: Dict[str, Any] = {
            "total_debates": 0,
            "active_sessions": [],
            "debate_history": [],
            "agent_performance": {
                "Agent 1": {"wins": 0, "losses": 0, "ties": 0},
                "Agent 2": {"wins": 0, "losses": 0, "ties": 0}
            }
        }
    
    def create_context(self, topic: str, agent1_position: str, agent2_position: str, 
                       max_rounds: int = 3) -> str:
        """Create a new debate context"""
        session_id = str(uuid.uuid4())
        
        context = DebateContext(
            session_id=session_id,
            topic=topic,
            agent1_position=agent1_position,
            agent2_position=agent2_position,
            agent1_arguments=[],
            agent2_arguments=[],
            current_round=1,
            max_rounds=max_rounds,
            timestamp=datetime.now().isoformat(),
            metadata={
                "status": "active",
                "winner": None,
                "reasoning": None
            }
        )
        
        self.contexts[session_id] = context
        self.global_context["total_debates"] += 1
        self.global_context["active_sessions"].append(session_id)
        
        return session_id
    
    def get_context(self, session_id: str) -> Optional[DebateContext]:
        """Retrieve debate context by session ID"""
        return self.contexts.get(session_id)
    
    def update_context(self, session_id: str, **kwargs) -> bool:
        """Update debate context with new information"""
        if session_id not in self.contexts:
            return False
        
        context = self.contexts[session_id]
        
        for key, value in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, value)
            elif key in context.metadata:
                context.metadata[key] = value
        
        return True
    
    def add_argument(self, session_id: str, agent: str, argument: str) -> bool:
        """Add an argument to the debate context"""
        if session_id not in self.contexts:
            return False
        
        context = self.contexts[session_id]
        
        if agent == "Agent 1":
            context.agent1_arguments.append(argument)
        elif agent == "Agent 2":
            context.agent2_arguments.append(argument)
        else:
            return False
        
        return True
    
    def get_relevant_context(self, session_id: str, agent: str, 
                            round_num: int) -> Dict[str, Any]:
        """Get relevant context for an agent's decision making"""
        context = self.get_context(session_id)
        if not context:
            return {}
        
        opponent_args = (context.agent2_arguments if agent == "Agent 1" 
                        else context.agent1_arguments)
        
        return {
            "topic": context.topic,
            "agent_position": context.agent1_position if agent == "Agent 1" else context.agent2_position,
            "opponent_position": context.agent2_position if agent == "Agent 1" else context.agent1_position,
            "current_round": round_num,
            "opponent_arguments": opponent_args[-2:],  # Last 2 arguments
            "my_arguments": context.agent1_arguments if agent == "Agent 1" else context.agent2_arguments,
            "debate_progress": f"Round {round_num} of {context.max_rounds}",
            "topic_analysis": self._analyze_topic(context.topic)
        }
    
    def _analyze_topic(self, topic: str) -> Dict[str, Any]:
        """Analyze topic for additional context"""
        return {
            "word_count": len(topic.split()),
            "topic_type": self._classify_topic(topic),
            "complexity": "simple" if len(topic.split()) < 10 else "complex"
        }
    
    def _classify_topic(self, topic: str) -> str:
        """Classify the topic type"""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ["should", "regulate", "policy", "law"]):
            return "policy"
        elif any(word in topic_lower for word in ["better", "worse", "compare", "vs"]):
            return "comparison"
        elif any(word in topic_lower for word in ["ethical", "moral", "right", "wrong"]):
            return "ethical"
        elif any(word in topic_lower for word in ["technology", "ai", "computer"]):
            return "technology"
        else:
            return "general"
    
    def conclude_debate(self, session_id: str, winner: str, reasoning: str) -> bool:
        """Conclude a debate and update global context"""
        if session_id not in self.contexts:
            return False
        
        context = self.contexts[session_id]
        context.metadata["status"] = "completed"
        context.metadata["winner"] = winner
        context.metadata["reasoning"] = reasoning
        
        # Update global context
        if session_id in self.global_context["active_sessions"]:
            self.global_context["active_sessions"].remove(session_id)
        
        # Update agent performance
        if winner in ["Agent 1", "Agent 2"]:
            loser = "Agent 2" if winner == "Agent 1" else "Agent 1"
            self.global_context["agent_performance"][winner]["wins"] += 1
            self.global_context["agent_performance"][loser]["losses"] += 1
        else:
            self.global_context["agent_performance"]["Agent 1"]["ties"] += 1
            self.global_context["agent_performance"]["Agent 2"]["ties"] += 1
        
        # Add to history
        self.global_context["debate_history"].append({
            "session_id": session_id,
            "topic": context.topic,
            "winner": winner,
            "timestamp": context.timestamp,
            "rounds": context.current_round - 1
        })
        
        return True
    
    def get_agent_history(self, agent: str) -> List[Dict[str, Any]]:
        """Get performance history for a specific agent"""
        history = []
        
        for debate in self.global_context["debate_history"]:
            context = self.contexts.get(debate["session_id"])
            if context:
                agent_args = (context.agent1_arguments if agent == "Agent 1" 
                            else context.agent2_arguments)
                
                history.append({
                    "topic": debate["topic"],
                    "position": context.agent1_position if agent == "Agent 1" else context.agent2_position,
                    "arguments": agent_args,
                    "result": "win" if debate["winner"] == agent else "loss" if debate["winner"] in ["Agent 1", "Agent 2"] else "tie",
                    "rounds": debate["rounds"]
                })
        
        return history
    
    def export_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Export debate context for external use"""
        context = self.get_context(session_id)
        if not context:
            return None
        
        # Convert to dictionary manually to avoid issues with asdict
        return {
            "session_id": context.session_id,
            "topic": context.topic,
            "agent1_position": context.agent1_position,
            "agent2_position": context.agent2_position,
            "agent1_arguments": context.agent1_arguments,
            "agent2_arguments": context.agent2_arguments,
            "current_round": context.current_round,
            "max_rounds": context.max_rounds,
            "timestamp": context.timestamp,
            "metadata": context.metadata
        }
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Get global statistics"""
        return {
            "total_debates": self.global_context["total_debates"],
            "active_sessions": len(self.global_context["active_sessions"]),
            "agent_performance": self.global_context["agent_performance"],
            "recent_topics": [debate["topic"] for debate in self.global_context["debate_history"][-5:]]
        }

# Global MCP server instance
mcp_server = MCPServer()
