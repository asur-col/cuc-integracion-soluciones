import sys; sys.path.insert(0,'.')
import reg
import slides1
import gen
# slides faltantes: placeholders
for n in range(1,57):
    if n not in reg.SL: reg.slide(n, '<svg viewBox="0 0 1180 500"><text x="590" y="250" font-size="30" text-anchor="middle">pendiente</text></svg>')
import slides2,slides3,slides4
gen.render()
