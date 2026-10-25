from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/boreo-r07-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from slicer_utils import parse_gcode
from prepara_slicing_pla import COLORS
ROOT=Path(__file__).resolve().parents[1]
layers,analysis=parse_gcode(ROOT/'stampa/PLA_BASIC_ECC2/BOREO_R07_DIMA_PLA_BASIC_ECC2_04.gcode')
fig,axes=plt.subplots(3,2,figsize=(14,10),facecolor='white')
for ax,index in zip(axes.ravel(),[0,52,59,74,105,143]):
 l=layers[index];lines=[];colors=[]
 for x1,y1,x2,y2,role in l['segments']:
  lines.append([(x1,y1),(x2,y2)]);colors.append(COLORS.get(role,'#778892'))
 ax.add_collection(LineCollection(lines,colors=colors,linewidths=.7));ax.set_xlim(72,184);ax.set_ylim(78,114);ax.set_aspect('equal');ax.set_title(f"Base: strato {l['number']}, Z {l['z_mm']:.2f} mm");ax.grid(alpha=.15)
fig.suptitle('R07: percorsi reali, dettaglio supporti, sedi dadi e passaggi',fontsize=16)
fig.tight_layout();fig.savefig(ROOT/'anteprime/slicing/dettagli_giunto.png',dpi=140)
