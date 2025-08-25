import os
from pandas import DataFrame as DF, read_csv
os.chdir(os.path.abspath(os.path.dirname(__file__)))#解析进入程序所在目录
fp_last = "20212022.csv"
fp_current = "20222023.csv"
fp_common_last = "c20212022.csv"
fp_common_current = "c20222023.csv"
fp_contrast = "contrast.csv"

# 读取表格
pf_last = read_csv(fp_last)
pf_current = read_csv(fp_current)
columns = list(pf_last.columns)
print("表头字段：{0}".format(columns))

# 获取共同 ID
id_last = pf_last["ID"].tolist()
id_current = pf_current["ID"].tolist()
id_common = []
for id in id_last:
	if id in id_current:
		id_common.append(id)
id_common = list(set(id_common))
print("2021-2022 学年共有 {0} 条数据，2022-2023 学年共有 {1} 条数据，两学年共有的数据有 {0} 条。".format(len(id_last), len(id_current), len(id_common)))

# 处理比较
common_last = []
common_current = []
def handleTmp(tmp):
	tmp[0] = int(tmp[0])
	tmp[1] = tmp[1] % 2
	tmp[2] = tmp[3] / (tmp[2] / 100) ** 2
	del tmp[3]
	return tmp
for id in id_common:
	common_last.append(handleTmp(pf_last[pf_last["ID"] == id].values.tolist()[0]))
	common_current.append(handleTmp(pf_current[pf_current["ID"] == id].values.tolist()[0]))
columns[2] = "BMI"
del columns[3]
pf_common_last  = DF(common_last, columns = columns)
pf_common_current = DF(common_current, columns = columns)
pf_common_last.to_csv(fp_common_last, index = False)
pf_common_current.to_csv(fp_common_current, index = False)
pf_common_current["BMI"] = (abs(pf_common_last["BMI"] - 21.2) - abs(pf_common_current["BMI"] - 21.2)) / abs(pf_common_last["BMI"] - 21.2) # 差值越小越好
pf_common_current["lung"] = (pf_common_current["lung"] - pf_common_last["lung"]) / pf_common_last["lung"]
pf_common_current["shortRun"] = (pf_common_last["shortRun"] - pf_common_current["shortRun"]) / pf_common_last["shortRun"] # 跑步速度越快越好
pf_common_current["jump"] = (pf_common_current["jump"] - pf_common_last["jump"]) / pf_common_last["jump"]
pf_common_current["knee"] = (pf_common_current["knee"] - pf_common_last["knee"]) / pf_common_last["knee"]
pf_common_current["longRun"] = (pf_common_last["longRun"] - pf_common_current["longRun"]) / pf_common_last["longRun"] # 跑步速度越快越好
pf_common_current["upDown"] = (pf_common_current["upDown"] - pf_common_last["upDown"]) / pf_common_last["upDown"]
pf_common_current.to_csv(fp_contrast, index = False)