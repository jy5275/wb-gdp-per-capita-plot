import sqlite3, math
import matplotlib.pyplot as plt
import numpy as np

sql = """select t2.Year as Year, t1.CountryName, t2.CountryName, t1.Value as v1, t2.Value as v2 from 
(select CountryName, Value, Year from gdp_per_capital where CountryName='%s') t1 RIGHT JOIN 
(select CountryName, Value, Year from gdp_per_capital where CountryName='China') t2 ON t1.Year=t2.Year 
order by Year asc
"""

conn = sqlite3.connect('data.db')
country_list = ["Canada","Japan","Korea, Rep.","Singapore","Thailand","Malaysia"]
# country_list = ["World","East Asia & Pacific","Europe & Central Asia","Middle East & North Africa","Sub-Saharan Africa","Latin America & Caribbean"]
arg_list = ["b,-", "r,:", "g,:", "c,--", "m,:", "k,:","y,:"]
years = np.arange(1960, 2023)

for idx, c in enumerate(country_list):
	cursor = conn.cursor()
	cursor.execute(sql % c)
	results = cursor.fetchall()
	data = [[row[0], row[1], row[2], row[3], row[4]] for row in results]
	ratio = []
	for r in data:
		if r[3] == 0 or r[3] is None:
			ratio.append(None)
		else:
			val = r[3] / r[4]
			ratio.append(math.log10(val))
	
	print(c, len(years), ratio[:5])
	plt.plot(years, ratio, arg_list[idx], alpha=0.5, linewidth=1, label=c)

conn.close()

plt.legend()
plt.xlabel('year')
plt.ylabel('log(ratio)')
plt.title('GDP per capita comparison: others / China')
#plt.ylim(-1,1)
plt.grid()
plt.show()
