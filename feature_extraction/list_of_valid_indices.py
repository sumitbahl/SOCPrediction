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

good_indices_short_names = []
good_indices_long_names =[]
good_indices_formulas = []
good_indices_references = []

for i, x in enumerate(list(df['short_name'])):
	valid = True
	for bad in bad_vars:
		if bad in formulas[i]:
			valid = False
	if (valid):
		good_indices_short_names.append(x)
		good_indices_long_names.append(list(df['long_name'])[i])
		good_indices_formulas.append(list(df['formula'])[i])
		good_indices_references.append(list(df['reference'])[i])


df = pd.DataFrame({
	'short_name' : good_indices_short_names,
	'long_name' : good_indices_long_names,
	'formula' : good_indices_formulas,
	'reference' : good_indices_references
})

df.to_csv("valid_indices.csv", index = False)
