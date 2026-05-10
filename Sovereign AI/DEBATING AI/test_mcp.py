from mcp_server import mcp_server

print('Testing MCP functionality...')

# Create a test session
session_id = mcp_server.create_context('Test topic', 'FOR', 'AGAINST', 3)
print(f'Created session: {session_id}')

# Add some arguments
mcp_server.add_argument(session_id, 'Agent 1', 'This is a test argument for agent 1')
mcp_server.add_argument(session_id, 'Agent 2', 'This is a test argument for agent 2')

# Get context
context = mcp_server.get_context(session_id)
print(f'Context retrieved: {context is not None}')
if context:
    print(f'Topic: {context.topic}')

# Get relevant context for agent 1
rel_context = mcp_server.get_relevant_context(session_id, 'Agent 1', 1)
print(f'Relevant context keys: {list(rel_context.keys())}')

# Conclude debate
mcp_server.conclude_debate(session_id, 'Agent 1', 'Agent 1 had better arguments')

# Get final stats
stats = mcp_server.get_global_stats()
print(f'Final total debates: {stats["total_debates"]}')
print('MCP is working correctly!')
