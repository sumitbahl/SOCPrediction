f = open("r_script_commands_list.txt", "w")

for lat in range(-90, 89, 2):
	for long in range(-180, 179, 2):
		f.write(f"Rscript HWSD.r {long} {long + 2} {lat + 2} {lat}\n")

f.close()