"""
Goblin Markdown Converter Core v1.0
Core library for converting Goblin Tools task lists to Markdown.
"""

import json
import datetime
import sys
import os

def format_duration(seconds):
    """Convert seconds to a human-readable duration string."""
    if not seconds:
        return ""
    
    # Calculate days, hours, minutes
    days = seconds // (24 * 3600)
    remaining = seconds % (24 * 3600)
    hours = remaining // 3600
    remaining = remaining % 3600
    minutes = remaining // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if not parts:  # For very short durations
        parts.append("1m")
    
    return " ".join(parts)

def format_estimate(estimate):
    """Format the time estimate to a string."""
    if not estimate:
        return ""
    duration = format_duration(estimate)
    return f" ({duration})" if duration else ""

def format_timestamp(timestamp):
    """Format timestamp to a readable date."""
    if not timestamp:
        return ""
    
    # Convert milliseconds to seconds if needed
    if timestamp > 1000000000000:  # If timestamp is in milliseconds
        timestamp = timestamp / 1000
    
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, TypeError):
        return ""

def get_task_category_emoji(category):
    """Map category to emoji.
    
    Categories from Goblin Tools Magic ToDo:
    ☑️ - General/Default tasks
    🛠 - Technical/Development tasks
    📋 - Organization/Planning tasks
    🎨 - Creative/Design tasks
    🏢 - Business/Corporate tasks
    📈 - Analytics/Growth tasks
    🤝 - Social/Collaboration tasks
    📚 - Learning/Research tasks
    🖊 - Writing/Content tasks
    🎓 - Education/Academic tasks
    💬 - Communication/Discussion tasks
    📝 - Documentation/Notes tasks
    💵 - Financial/Money tasks
    """
    emoji_map = {
        "☑️": "☑️",  # General/Default
        "🛠": "🛠",   # Technical/Development
        "📋": "📋",  # Organization/Planning
        "🎨": "🎨",  # Creative/Design
        "🏢": "🏢",  # Business/Corporate
        "📈": "📈",  # Analytics/Growth
        "🤝": "🤝",  # Social/Collaboration
        "📚": "📚",  # Learning/Research
        "🖊": "🖊",   # Writing/Content
        "🎓": "🎓",  # Education/Academic
        "💬": "💬",  # Communication/Discussion
        "📝": "📝",  # Documentation/Notes
        "💵": "💵"   # Financial/Money
    }
    return emoji_map.get(category, "☑️")  # Return default emoji if category not found

def process_tasks(tasks):
    """Process tasks and return a dictionary of parent-child relationships."""
    task_dict = {}
    root_tasks = []
    
    # First pass: Create dictionary of all tasks
    for task in tasks:
        task_dict[task['id']] = {
            'task': task,
            'children': []
        }
    
    # Second pass: Build parent-child relationships
    for task in tasks:
        if task['parentId'] is None:
            root_tasks.append(task_dict[task['id']])
        else:
            parent = task_dict.get(task['parentId'])
            if parent:
                parent['children'].append(task_dict[task['id']])
    
    return root_tasks

def generate_markdown(task_node, level=0, show_timestamps=False):
    """Generate markdown for a task and its children."""
    task = task_node['task']
    children = task_node['children']
    indent = "  " * level
    
    # Get emoji if it's a root task
    emoji = get_task_category_emoji(task.get('category', '')) if level == 0 else ""
    
    # Check if task is completed
    is_completed = task.get('completed', False)
    checkbox = "[x]" if is_completed else "[ ]"
    
    # Format the task line
    task_line = f"{indent}- {checkbox} {task['text']}{format_estimate(task.get('estimate'))}"
    
    # Add timestamp if requested
    if show_timestamps and task.get('timestamp'):
        timestamp = format_timestamp(task.get('timestamp'))
        if timestamp:
            task_line += f" (Created: {timestamp})"
    
    # For root tasks, add a header
    if level == 0:
        lines = [f"\n## {emoji} {task['text']}{format_estimate(task.get('estimate'))}"]
    else:
        lines = [task_line]
    
    # Add children
    for child in children:
        lines.extend(generate_markdown(child, level + 1, show_timestamps))
    
    return lines

def convert_json_to_markdown(json_data, show_timestamps=False):
    """Convert JSON task data to markdown format."""
    # Parse JSON if it's a string
    if isinstance(json_data, str):
        tasks = json.loads(json_data)
    else:
        tasks = json_data
    
    # Process tasks into a tree structure
    root_tasks = process_tasks(tasks)
    
    # Generate markdown
    markdown_lines = ["# Tasks"]
    for task_node in root_tasks:
        markdown_lines.extend(generate_markdown(task_node, show_timestamps=show_timestamps))
    
    return "\n".join(markdown_lines)

def get_output_filename(input_file):
    """Generate output filename based on input filename."""
    base_name = os.path.splitext(input_file)[0]
    return f"{base_name}.md"

def process_canvas_to_tasks(canvas_data):
    """Convert Obsidian canvas data to task format."""
    tasks = []
    node_map = {}
    
    # First pass: Create task entries for all nodes
    for node in canvas_data.get('nodes', []):
        if node.get('type') == 'text':
            task = {
                'id': node['id'],
                'parentId': None,  # Will be updated in second pass
                'text': node.get('text', ''),
                'timestamp': int(datetime.datetime.now().timestamp() * 1000),  # Current timestamp
                'category': '📝'  # Default category for canvas items
            }
            tasks.append(task)
            node_map[node['id']] = task
    
    # Second pass: Process edges to establish parent-child relationships
    for edge in canvas_data.get('edges', []):
        from_node = node_map.get(edge['fromNode'])
        to_node = node_map.get(edge['toNode'])
        
        if from_node and to_node:
            to_node['parentId'] = from_node['id']
    
    return tasks

def convert_tasks_to_canvas(tasks):
    """Convert task data to Obsidian canvas format."""
    nodes = []
    edges = []
    node_map = {}
    
    # First pass: Create nodes for all tasks and identify root tasks
    root_tasks = []
    for task in tasks:
        # Format the card text with emoji and time estimate
        emoji = get_task_category_emoji(task.get('category', ''))
        time_estimate = format_estimate(task.get('estimate', 0))
        card_text = f"{emoji} {task['text']}{time_estimate}"
        
        node = {
            'id': task['id'],
            'type': 'text',
            'text': card_text,
            'width': 400,
            'height': 100,
            'color': '1'
        }
        nodes.append(node)
        node_map[task['id']] = node
        if task['parentId'] is None:
            root_tasks.append(task)
    
    # Calculate layout
    HORIZONTAL_SPACING = 500  # Space between parent tasks
    VERTICAL_SPACING = 150    # Space between parent and children
    CHILD_SPACING = 120      # Space between sibling tasks
    
    # Position root tasks horizontally
    for i, task in enumerate(root_tasks):
        node = node_map[task['id']]
        node['x'] = i * HORIZONTAL_SPACING
        node['y'] = 0
        
        # Position children vertically below their parent
        children = [t for t in tasks if t['parentId'] == task['id']]
        for j, child in enumerate(children):
            child_node = node_map[child['id']]
            child_node['x'] = node['x']  # Align with parent
            child_node['y'] = node['y'] + VERTICAL_SPACING + (j * CHILD_SPACING)
    
    # Create edges for parent-child relationships
    for task in tasks:
        if task['parentId'] is not None:
            edge = {
                'id': f"{task['parentId']}-{task['id']}",
                'fromNode': task['parentId'],
                'toNode': task['id'],
                'label': ''
            }
            edges.append(edge)
    
    return {
        'nodes': nodes,
        'edges': edges
    }

def get_input_file():
    """Prompt user for input file and validate it exists."""
    while True:
        input_file = input("\nEnter the path to your .goblin or .json file: ").strip()
        if not input_file:
            print("Please enter a file path.")
            continue
            
        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' not found!")
            continue
            
        _, ext = os.path.splitext(input_file)
        if ext.lower() not in ['.json', '.goblin']:
            print("Error: Please use a .json or .goblin file.")
            continue
            
        return input_file

def get_output_format():
    """Prompt user for desired output format."""
    while True:
        print("\nWhat would you like to convert to?")
        print("1. Markdown (tasks.md)")
        print("2. Canvas (tasks.canvas)")
        print("3. Both formats")
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice in ['1', '2', '3']:
            return choice
        print("Please enter 1, 2, or 3.")

def get_timestamp_option():
    """Prompt user about including timestamps in markdown output."""
    while True:
        choice = input("\nInclude timestamps in markdown output? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("Please enter 'y' or 'n'.")

def detect_file_format(file_path):
    """Detect the format of the input file based on its extension."""
    _, ext = os.path.splitext(file_path)
    return ext.lower()

def read_input_file(file_path):
    """Read and parse the input file based on its format."""
    file_format = detect_file_format(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if file_format == '.goblin':
            # Goblin files are JSON arrays of tasks
            return json.loads(content)
        elif file_format == '.json':
            data = json.loads(content)
            # Check if it's a canvas format (has nodes and edges)
            if 'nodes' in data and 'edges' in data:
                return process_canvas_to_tasks(data)
            # Otherwise assume it's a direct task array
            return data
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing {file_format} file: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

def main():
    """Main function to convert task files to markdown."""
    try:
        # Get input file
        input_file = get_input_file()
        if not input_file:
            print("No input file specified. Please provide a .goblin or .json file.")
            return

        # Read and process the input file
        tasks = read_input_file(input_file)
        
        # Get output format and timestamp option
        output_format = get_output_format()
        show_timestamps = get_timestamp_option()
        
        # Generate output
        if output_format == 'markdown':
            output = convert_json_to_markdown(tasks, show_timestamps)
            output_file = get_output_filename(input_file)
        else:  # canvas format
            output = json.dumps(convert_tasks_to_canvas(tasks), indent=2)
            output_file = os.path.splitext(input_file)[0] + '.canvas'
        
        # Write output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
            
        print(f"Successfully converted {input_file} to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 