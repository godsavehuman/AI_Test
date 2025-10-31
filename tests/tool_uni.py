from tooluniverse import ToolUniverse

# Initialize ToolUniverse
tu = ToolUniverse()

# Load all tools from all categories
tu.load_tools()

# Check how many tools were loaded
print(f"Loaded {len(tu.all_tools)} tools")

# List first 5 tools
tool_names = tu.list_built_in_tools(mode='list_name')
for tool in tool_names[:5]:
    print(f"  • {tool}")
