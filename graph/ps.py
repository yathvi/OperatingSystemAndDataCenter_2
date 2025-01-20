import subprocess
from graphviz import Digraph
import os

def get_ps_output():
    try:
        # Launch the ps command using subprocess.Popen
        process = subprocess.Popen(["ps", "-eT", "-o", "ppid,pid,tid,user,comm"], stdout=subprocess.PIPE)
        
        # Get the PID of the ps command
        ps_pid = process.pid
        
        # Retrieve the output
        ps_output, _ = process.communicate()
        
        return ps_output.decode("utf-8"), ps_pid
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        return None, None

ps_output, ps_pid = get_ps_output()
current_pid = os.getpid()
print("os.getpid()", current_pid)
print("os.getppid()", os.getppid())
print("ps_pid", ps_pid)

if ps_output:
    lines = ps_output.split('\n')[1:]  # Skip header
    dot = Digraph()

    process_info = {}  # Dictionary to store process info by PID
    # Initialize a set to store unique edge pairs
    unique_edges = set()

    for line in lines:
        parts = line.split()
        if len(parts) >= 5:
            print("pr")
            ppid, pid, tid, user = parts[:4]
            comm_list = parts[4:]
            comm = ' '.join(comm_list)  # Join the command parts into a single string
            
            # Exclude the PID associated with the ps command
            if str(pid) != str(ps_pid)  and str(ppid) != str(ps_pid) and str(tid) != str(ps_pid) and str(pid) != str(current_pid) and str(ppid) != str(current_pid) and tid != current_pid:
                print(ppid," -> ",pid," -> ",tid," <---> ",current_pid," -> ",ps_pid)
                process_info[tid] = {'ppid': ppid, 'pid':pid, 'user': user, 'comm': comm}
    

    for tid, info in process_info.items():
        print(tid,info)
        node_label = f"{tid} {info['user']}\n{info['comm']}"
        # Check if PID is equal to TID
        if str(info['pid']) == str(tid):
            # Add color to the node
            dot.node(tid, node_label, color='red', fillcolor='lightblue', style='filled')  # Adjust color as needed
        else:
            # Add the node without color
            dot.node(tid, node_label)
        
        # Include user information for the parent process as well
        parent_user = process_info.get(info['pid'], {}).get('user', '')
        dot.node(info['pid'], f"{info['pid']} {parent_user}\n{process_info.get(info['pid'], {}).get('comm', '')}")
        
        if str(info['pid']) != str(tid):# Avoid adding self loops
            dot.edge(info['pid'], tid)
        
        # Add edges from PPID to PID
        if str(info['ppid']) != str(info['pid']) and (info['ppid'], info['pid']) not in unique_edges:# Avoid adding self loops and  Check if the edge pair (PPID, PID) is not already in the set
            dot.edge(info['ppid'], info['pid'])
            # Add the edge pair to the set
            unique_edges.add((info['ppid'], info['pid']))

    try:
        # Set graph attributes
        dot.attr(rankdir='LR')
        
        dot.render('process_graph', format='png', view=False)
        dot.render('process_graph', format='jpg', view=False)
        dot.render('process_graph', format='pdf', view=False)
    except Exception as e:
        print("Error rendering graph:", e)
