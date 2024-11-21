# 单线程
import subprocess
import os

def pull_latest_code(repo_path):
    try:
        result = subprocess.run(['git', '-C', repo_path, 'pull'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"成功拉取最新代码: {repo_path}")
        else:
            print(f"拉取最新代码失败: {repo_path}\n{result.stderr}")
    except Exception as e:
        print(f"拉取最新代码时出错: {e}")

def get_last_commit_id(repo_path, branch):
    try:
        # 切换到仓库目录
        os.chdir(repo_path)
        print(f"切换到目录: {repo_path}")
        
        # 切换到指定分支
        subprocess.run(['git', 'checkout', branch], check=True, shell=True)
        print(f"切换到分支: {branch}")
        
        # 获取最后一次提交的commit id
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True, shell=True, encoding='utf-8')
        print(f"获取到的commit id: {result.stdout.strip()}")
        
        return result.stdout.strip()
    except Exception as e:
        print(f"获取提交ID时出错: {e}")
        return None

def write_commit_id_to_file(repo_name, commit_id, filename):
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(f"Repository: {repo_name}\n")
            file.write(f"Commit ID: {commit_id}\n")
            file.write("\n" + "="*40 + "\n")
        print(f"写入 {repo_name} 的提交ID: {commit_id}")
    except Exception as e:
        print(f"写入文件时出错: {e}")

if __name__ == "__main__":
    # 仓库都在同一个目录下，修改此处，否则修改repositories列表
    absPath = 'D:\\IFS_V1.50.02.00-C'
    # 分支名称
    branchName = 'IFS_V1.50.02.00-C'
    repositories = [
        {'name': 'are-alarm-web', 'path': absPath, 'branch': branchName},
        {'name': 'are-client', 'path': absPath, 'branch': branchName},
        {'name': 'are-flowchart-web', 'path': absPath, 'branch': branchName},
        {'name': 'are-trend-web', 'path': absPath, 'branch': branchName},
        {'name': 'are-log-service-web', 'path': absPath, 'branch': branchName},
        {'name': 'are-utils-web', 'path': absPath, 'branch': branchName},
        {'name': 'basic-root-config', 'path': absPath, 'branch': branchName},
        {'name': 'fusionsite-are-diagnosis-web', 'path': absPath, 'branch': branchName},
        {'name': 'mare-basic-web', 'path': absPath, 'branch': branchName},
        {'name': 'mare-common-web', 'path': absPath, 'branch': branchName},
        {'name': 'resexplorer', 'path': absPath, 'branch': branchName},
        {'name': 'unifiedconfigtool', 'path': absPath, 'branch': branchName},
        {'name': 'electric-control', 'path': absPath, 'branch': branchName},
        {'name': 'params-config-web', 'path': absPath, 'branch': branchName},
        {'name': 'tsi-log-tool-web', 'path': absPath, 'branch': branchName},
        {'name': 'fsauthorizationtool', 'path': absPath, 'branch': branchName},
        # 添加更多仓库信息
    ]
    output_file = os.path.abspath('last_commit_ids.txt')
    print(f"输出文件: {output_file}")
    # 清空输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("")
        print(f"清空文件: {output_file}")
    except Exception as e:
        print(f"清空文件时出错: {e}")
    
    for repo in repositories:
        repo_name = repo['name']
        repo_path = repo['path'] + "\\" + repo_name
        branch_name = repo['branch']
        
        try:
            print(f"正在处理仓库: {repo_name}, 分支: {branch_name}")
            pull_latest_code(repo_path)
            commit_id = get_last_commit_id(repo_path, branch_name)
            if commit_id:
                write_commit_id_to_file(repo_name, commit_id, output_file)
                print(f"{repo_name} 的最后一次提交ID已写入 {output_file}")
            else:
                print(f"{repo_name} 没有找到提交记录")
        except subprocess.CalledProcessError as e:
            print(f"获取 {repo_name} 的提交记录时出错: {e}")
        except Exception as e:
            print(f"处理 {repo_name} 时发生意外错误: {e}")