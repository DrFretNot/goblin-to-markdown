"""
Goblin Markdown Converter CLI v1.0
A command-line interface for converting Goblin Tools task lists to Markdown.
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

def main():
    # Get input file from command line argument or use default
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'tasks.json'
    
    # Check if timestamps should be shown
    show_timestamps = "--timestamps" in sys.argv or "-t" in sys.argv
    
    # Check if we should create a canvas file
    create_canvas = "--canvas" in sys.argv or "-c" in sys.argv
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return
    
    # Get file extension
    _, ext = os.path.splitext(input_file)
    
    try:
        # Read file content
        with open(input_file, 'r', encoding='utf-8') as f:
            if ext.lower() in ['.json', '.goblin']:
                json_data = json.load(f)
                # Check if it's a canvas file by looking for nodes and edges
                if isinstance(json_data, dict) and 'nodes' in json_data and 'edges' in json_data:
                    json_data = process_canvas_to_tasks(json_data)
            else:
                print(f"Error: Unsupported file extension {ext}. Please use .json or .goblin files.")
                return
        
        if create_canvas:
            # Convert to canvas format
            canvas_data = convert_tasks_to_canvas(json_data)
            
            # Generate output filename
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.canvas"
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(canvas_data, f, indent=2)
                
            print(f"Successfully converted {input_file} to {output_file}!")
        else:
            # Convert to markdown
            markdown = convert_json_to_markdown(json_data, show_timestamps=show_timestamps)
            
            # Generate output filename
            output_file = get_output_filename(input_file)
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown)
                
            print(f"Successfully converted {input_file} to {output_file}!")
        
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {input_file}!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 