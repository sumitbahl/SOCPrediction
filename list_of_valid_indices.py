import pandas as pd

df = pd.read_csv("/mnt/chromeos/MyFiles/Coding/SOCPrediction/spectral-indices-table.csv")

bad_vars = [
	"cexp",
	"nexp",
	"alpha",
	"beta",
	"gamma",
	"omega",
	"sla",
	"slb",
	"PAR",
	"k",
	"lambdaN",
	"lambdaR",
	"lambdaG",
	"RE1",
	"RE2",
	"RE3",
	"N2",
	"HV",
	"VH",
	"HH",
	"VV",
	"kAB",
	"p",
	"c",
	"fdelta"
]

formulas = list(df['bands'])

good_indices = []

for i, x in enumerate(list(df['short_name'])):
	valid = True
	for bad in bad_vars:
		if bad in formulas[i]:
			valid = False
	if (valid):
		good_indices.append(x)

print(good_indices)
