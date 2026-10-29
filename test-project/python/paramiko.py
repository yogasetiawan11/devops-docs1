import paramiko

def run_remote_command(hostname, username, password, command):
    # Initialize SSH client
    ssh = paramiko.SSHClient()
    
    # Automatically add the server's SSH key (Use with caution in production)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the server
        ssh.connect(hostname=hostname, username=username, password=password, timeout=10)
        
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Read the output and errors
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if error:
            print(f"Error executing command:\n{error}")
        else:
            print(f"Command Output:\n{output}")
            
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        # Always close the connection
        ssh.close()

# Example Usage
run_remote_command('192.168.1.50', 'deploy_user', 'secure_password', 'sudo systemctl restart nginx')
