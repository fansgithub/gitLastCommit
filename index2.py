# 多线程
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def pull_latest_code(repo_path):
    try:
        result = subprocess.run(['git', '-C', repo_path, 'pull'], capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"成功拉取最新代码: {repo_path}")
        else:
            print(f"拉取最新代码失败: {repo_path}\n{result.stderr}")
    except Exception as e:
        print(f"拉取最新代码时出错: {e}")

def switch_to_branch(repo_path, branch_name):
    try:
        subprocess.run(
            ["git", "-C", repo_path, "checkout", branch_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"{repo_path} 切换到分支: {branch_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error switching to branch {branch_name} for {repo_path}: {e}")

def get_last_commit_id(repo_path, branch_name):
    switch_to_branch(repo_path, branch_name)
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        print(f"获取到的Commit ID: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"获取 {repo_path} 提交ID时出错: {e}")
        return None

def process_repository(index, repo):
    pull_latest_code(repo['path']+ "\\" + repo['name'])
    commit_id = get_last_commit_id(repo['path']+ "\\" + repo['name'], repo['branch'])
    result = f"Processed: {repo['name']}\nCommit ID: {commit_id}"
    return index, result
        
def main(repositories):
    output_file = os.path.abspath('last_commit_ids.txt')
    # 清空输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("")
        print(f"清空文件: {output_file}")
    except Exception as e:
        print(f"清空文件时出错: {e}")
    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_repository, index, repo) for index, repo in enumerate(repositories)]
        for future in as_completed(futures):
          results.append(future.result())
    # 根据仓库索引排序结果
    results.sort(key=lambda x: x[0])

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, result in results:
            file.write(f"{result}\n")

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
    main(repositories)