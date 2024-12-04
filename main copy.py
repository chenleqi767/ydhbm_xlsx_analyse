import pandas as pd

# 读取文件
fileData = pd.read_csv("input.csv", encoding="gbk")

# 初始化一个新的 DataFrame 来存储每个人和其项目
project_list = []

# 遍历每一行，提取姓名和项目
for index, row in fileData.iterrows():
    name = row["姓名"]
    for i in range(1, 6):  # 遍历 "参赛项目1" 到 "参赛项目5"
        project_column = f"参赛项目{i}"
        project = row.get(project_column)
        if pd.notna(project):  # 如果项目非空
            project_list.append({"姓名": name, "参赛项目": project})

# 转换为 DataFrame
projects_df = pd.DataFrame(project_list)

# 打印提取后的项目数据
print(projects_df)

# 保存为 CSV 文件
projects_df.to_csv("extracted_projects.csv", index=False, encoding="utf-8-sig")
print("提取结果已保存到 extracted_projects.csv")

# 动态获取所有唯一的参赛项目
unique_projects = projects_df["参赛项目"].unique()

# 初始化一个字典来存储每个项目的参与者
project_participants = {project: [] for project in unique_projects}

# 遍历提取后的 DataFrame，根据项目分类存储姓名
for _, row in projects_df.iterrows():
    name = row["姓名"]
    project = row["参赛项目"]
    project_participants[project].append(name)

# 转换为 DataFrame
output_data = []
for project, participants in project_participants.items():
    output_data.append({
        "项目": project,
        "报名人数": len(participants),
        "报名人名单": "，".join(participants)
    })

project_summary_df = pd.DataFrame(output_data)

# 打印每个项目的报名情况
print(project_summary_df)

# 保存到文件
project_summary_df.to_csv("project_participants_summary.csv", index=False, encoding="utf-8-sig")
print("每个项目的报名情况已保存到 project_participants_summary.csv")


# 读取总名单文件
namelist_df = pd.read_csv("namelist.csv", encoding="gbk", header=None, names=["姓名"])

# 创建一个包含所有唯一项目的列表
unique_projects = projects_df["参赛项目"].unique()

# 初始化一个新的 DataFrame，列为运动项目，行是每个名字
attendance_df = pd.DataFrame(0, index=namelist_df["姓名"], columns=unique_projects)

# 遍历每个报名数据，填写对应的运动项目
for _, row in projects_df.iterrows():
    name = row["姓名"]
    project = row["参赛项目"]
    if name in attendance_df.index:  # 如果姓名在总名单中
        attendance_df.at[name, project] = 1  # 对应项目填1

# 打印新的报名情况表格
print(attendance_df)

# 保存新的表格为 CSV 文件
attendance_df.to_csv("attendance_by_project.csv", encoding="utf-8-sig")
print("总名单与项目对应的报名情况已保存到 attendance_by_project.csv")
