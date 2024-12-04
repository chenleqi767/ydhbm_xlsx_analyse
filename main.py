import pandas as pd

fileData = pd.read_csv("input.csv", encoding="gbk")

project_list = []

for index, row in fileData.iterrows():
    name = row["姓名"]
    for i in range(1, 6):
        project_column = f"参赛项目{i}"
        project = row.get(project_column)
        if pd.notna(project):
            project_list.append({"姓名": name, "参赛项目": project})

projects_df = pd.DataFrame(project_list)

projects_df.to_csv("extracted_projects.csv", index=False, encoding="utf-8-sig")

unique_projects = projects_df["参赛项目"].unique()

project_participants = {project: [] for project in unique_projects}

for _, row in projects_df.iterrows():
    name = row["姓名"]
    project = row["参赛项目"]
    project_participants[project].append(name)

output_data = []
for project, participants in project_participants.items():
    output_data.append({
        "项目": project,
        "报名人数": len(participants),
        "报名人名单": "，".join(participants)
    })

project_summary_df = pd.DataFrame(output_data)

namelist_df = pd.read_csv("namelist.csv", encoding="gbk", header=None, names=["姓名"])

attendance_df = pd.DataFrame(0, index=namelist_df["姓名"], columns=unique_projects)

for _, row in projects_df.iterrows():
    name = row["姓名"]
    project = row["参赛项目"]
    if name in attendance_df.index:
        attendance_df.at[name, project] = 1

with pd.ExcelWriter("output_results.xls", engine="xlsxwriter") as writer:
    projects_df.to_excel(writer, sheet_name="提取项目", index=False)
    project_summary_df.to_excel(writer, sheet_name="项目报名情况", index=False)
    attendance_df.to_excel(writer, sheet_name="报名情况表", index=True)

print("所有结果已保存到 output_results.xlsx")
