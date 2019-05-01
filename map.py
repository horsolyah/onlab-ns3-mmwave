import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib.ticker as ticker
#mplstyle.use('fast')
from matplotlib.patches import Rectangle, Circle, Arrow

'''
Box building_box = Box (50,55, -20,20, 0,50);
Vector UE_start_pos = Vector (100, -60.0, 1.5);
Vector UE_velocity_vector = Vector (0.0, 6.25, 0.0);
'''
'''
Box building_box = Box (50,55, 25,100, 0,50); 	// building -5 mely
	Box building_box_2 = Box (50,55, -100,-25, 0,50); 
	Vector UE_start_pos = Vector (100, -60.0, 1.5);
	Vector UE_velocity_vector = Vector (0.0, 6.25, 0.0)
'''

def add_building(x1, x2, y1, y2):
    width = x2 - x1
    height = y2 - y1
    building = Rectangle((x1, y1), width, height, linewidth=1, edgecolor='#222222', facecolor='#BBBBBB', antialiased=True, hatch='//')
    ax1.add_patch(building)

def add_node(x, y, color='b'):
    node = Circle((x, y), radius=3, linewidth=1, edgecolor='#222222', facecolor=color)
    ax1.add_patch(node)

def add_UE(x, y, vx, vy):
    add_node(x, y, 'b')
    arrow = Arrow(x, y, vx, vy, width=8.0, antialiased=False)
    ax1.add_patch(arrow)

#fig1 = plt.figure()
fig1 = plt.figure(figsize=(4, 4))
ax1 = fig1.add_subplot(111, aspect='equal')

#add_building(35,50, 20,30)
#add_building(35,50, -5,5)
#add_building(35,50, -20,-30)
add_building(37.5,50, 16.66,29.16)
add_building(37.5,50, -6.25,6.25)
add_building(37.5,50, -29.16,-16.66)
add_node(0, 0, 'r')
add_UE(75, -37.5, 0.0, 6.25)

ax1.xaxis.set_major_locator(ticker.MultipleLocator(25))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(25))
ax1.grid(color='#333333', linestyle=':', linewidth=1, antialiased=False, snap=True)
plt.ylim((-50, 50))
plt.xlim((0, 100))
#plt.show()
#plt.savefig('test.png', bbox_inches='tight', dpi=85)
plt.savefig('test.png', bbox_inches='tight')