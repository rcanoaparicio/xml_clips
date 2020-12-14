import csv

class Painting():
	def __init__(self, id, name, year, genre, artist, theme, x=0, y=0, complexity=0):
		self.id = int(id)
		self.name = name
		self.year = year
		self.genre = genre
		self.artist = int(artist)
		self.theme = theme
		self.x = x
		self.y = y
		self.complexity = complexity

class Autor():
	def __init__(self, id, name, nationality):
		self.id = int(id)
		self.name = name
		self.nationality = nationality
		self.visited = False
		self.styles = []
		self.themes = []

	def add_style(self, style):
		if not style in self.styles:
			self.styles.append(style)

	def add_theme(self, theme):
		if not theme in self.themes:
			self.themes.append(theme)

class Style():
	def __init__(self, id, name, nationality, start, end):
		self.id = int(id)
		self.name = name
		self.start = start
		self.end = end
		self.nationality = nationality
		self.visited = False

class Theme():
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.visited = False

paintings = []
autors = []
styles = []
themes = []

autor_template = ''
style_template = ''
painting_template = ''
theme_template = ''
xml_template = ''

with open('paintings.template', encoding='utf8') as f:
	painting_template = f.read()

themes_d = {}
with open('theme.template', encoding='utf8') as f:
	theme_template = f.read()

with open('style.template', encoding='utf8') as f:
	style_template = f.read()

with open('autor.template', encoding='utf8') as f:
	autor_template = f.read()

with open('xml.template', encoding='utf8') as f:
	xml_template = f.read()

with open('artists.csv', encoding='utf8') as csvfile:
	d = csv.reader(csvfile)
	next(d)
	for r in d:
		autors.append(Autor(r[0], r[1], r[4]))

styles_d = {}
with open('styles.csv', encoding='utf8') as csvfile:
	d = csv.reader(csvfile)
	next(d)
	for r in d:
		styles_d[r[1]] = int(r[0])
		styles.append(Style(r[0], r[1], r[2], r[3].split('-')[0], r[3].split('-')[1]))

with open('paintings.csv', encoding='utf8') as csvfile:
	d = csv.reader(csvfile)
	next(d)
	for r in d:
		paintings.append(Painting(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]))


outputs = []

for p in paintings:
	style_id = styles_d[p.genre]
	if not p.theme in themes_d:
		themes_d[p.theme] = len(themes)
		themes.append(Theme(themes_d[p.theme], p.theme))
	theme_id = themes_d[p.theme]
	#p.theme = theme_id
	autors[p.artist].add_style(style_id)
	autors[p.artist].add_theme(theme_id)
	#print(autors[p.artist].styles)



for p in paintings:
	theme_id = themes_d[p.theme]
	theme_text = '<Theme p_id="Theme_{}"/>'.format(theme_id)
	if not themes[theme_id].visited:
		themes[theme_id].visited = True
		theme_text = theme_template.format(theme_id, themes[theme_id].name)

	style_id = styles_d[p.genre]
	style_text = '<Style p_idref = "Style_{}"/>'.format(style_id)
	if not styles[style_id].visited:
		styles[style_id].visited = True
		style_text = style_template.format(style_id, styles[style_id].name, styles[style_id].start, styles[style_id].end, styles[style_id].nationality)

	autor_text = '<Author p_idref="Author_{}"/>'.format(p.artist)
	if not autors[p.artist].visited:
		autors[p.artist].visited = True
		ss = ''
		print(autors[p.artist].styles)
		for s in autors[p.artist].styles:
			if not styles[s].visited:
				styles[s].visited = True
				ss += style_template.format(s, styles[s].name, styles[s].start, styles[s].end, styles[s].nationality)
			else:
				ss += '<Style p_idref = "Style_{}"/>'.format(s)
			ss += '\n'
		print(ss)
		tt = ''
		for t in autors[p.artist].themes:
			if not themes[t].visited:
				themes[t].visited = True
				tt += theme_template.format(t, themes[t].name)
			else:
				tt += '<Theme p_idref = "Theme_{}"/>'.format(t)
			tt += '\n'
		autor_text = autor_template.format(p.artist, autors[p.artist].name, autors[p.artist].nationality, ss, tt)

	outputs.append(painting_template.format(p.name, p.year, style_text, theme_text, autor_text, p.x, p.y, p.complexity))

result = xml_template.format('\n'.join(outputs))
print(outputs[0])
with open('result.xml', 'w+', encoding='utf8') as f:
	f.write(result)