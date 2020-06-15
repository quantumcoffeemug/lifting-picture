#!/usr/bin/env python

import tkinter as tk
from math import sqrt,floor,acos,atan,pi

#--------------------Arc diagram objects--------------------------------

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.picture = None
		self.radius = 5
	
	def coordinates(self):
		return [self.x,self.y]
	
	def move(self, event):
		self.x = event.x
		self.y = event.y

class Vertex(Point):
	def __init__(self, x, y, color):
		self.color = color
		Point.__init__(self, x, y)
	
	def draw(self, canvas, active=False,in_diagram=False):
		if self.picture != None:
			canvas.delete(self.picture)
		x = self.x
		y = self.y
		RADIUS = self.radius
		
		if active:
			self.picture = canvas.create_oval(x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS, fill=self.color, outline="magenta", width=3,tags='in_diagram')
		else:
			self.picture = canvas.create_oval(x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS, fill=self.color,tags='in_diagram')
	
	def _signed_angle(self, arc1, arc2):
		x1 = arc1.opposite_vertex(self).x - self.x
		y1 = arc1.opposite_vertex(self).y - self.y
		x2 = arc2.opposite_vertex(self).x - self.x
		y2 = arc2.opposite_vertex(self).y - self.y
		
		l1 = x1**2 + y1**2
		l2 = x2**2 + y2**2
		
		dot_product = (x1*x2 + y1*y2)/(l1*l2)
		theta = acos(dot_product)
		
		def sign(x):
			if x<0:
				return -1
			else:
				return 1
		
		if theta < pi/2:
			return sign(atan(dot_product))*theta
		else:
			return -sign(atan(dot_product))*theta
	
	def 
	
class Waypoint(Point):
	def __init__(self, x, y, circle=None):
		self.color = 'blue'
		self.circle = circle
		Point.__init__(self, x, y)
	
	def draw(self, canvas, active=False,in_diagram=False):
		if self.picture != None:
			canvas.delete(self.picture)
		x = self.x
		y = self.y
		RADIUS = self.radius
		
		if active:
			self.picture = canvas.create_oval(x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS, fill=self.color, outline="magenta", width=3,tags='in_diagram')
		else:
			self.picture = canvas.create_oval(x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS, fill=self.color,tags='in_diagram')
	
	def move(self, event):
		if self.circle != None:
			self.x,self.y = self.circle.project_on_boundary(event.x, event.y).coordinates()
		else:
			Point.move(self, event)

class Boundary:
	def __init__(self, *vertices):
		self.vertices = vertices
		self.picture = None
	
	def draw(self, canvas, color="white"):
		vertex_coords = []
		
		for vertex in self.vertices:
			vertex_coords.append(vertex.coordinates())
		
		if self.picture != None:
			canvas.delete(self.picture)
		self.picture = canvas.create_polygon(*vertex_coords, fill=color, outline="black",tags='in_diagram')
		
		for vertex in self.vertices:
			vertex.draw(canvas,in_diagram=True)
	
	def edges(self):
		edges = []
		
		for n in range(len(self.vertices)):
			edges.append(Arc(self.vertices[n],self.vertices[(n+1)%len(self.vertices)]))
		
		return edges
	
	def contains(self, x, y):
		edges = self.edges()
		
		intersection_count = 0
		for edge in edges:
			min_y = min(edge.v1.y,edge.v2.y)
			max_y = max(edge.v1.y,edge.v2.y)
			M = (edge.v2.x-edge.v1.x)/(edge.v2.y-edge.v1.y) #reciprocal of slope
			
			if min_y < y < max_y and x-edge.v1.x < M*(y-edge.v1.y):
				intersection_count += 1
		
		if intersection_count%2 == 0:
			return False
		else:
			return True

class Circle:
	def __init__(self, center, radius, fill='white', outline='black'):
		self.center = center
		self.radius = radius
		self.fill = fill
		self.outline = outline
		self.picture = None
	
	def draw(self, canvas, active=False):
		if self.picture != None:
			canvas.delete(self.picture)
		x,y = self.center
		RADIUS = self.radius
		tag = 'in_diagram'
		
		if active:
			self.picture = canvas.create_oval(x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS, fill=self.fill, outline='magenta', width=4,tags=tag)
		else:
			self.picture = canvas.create_oval(x-RADIUS, y-RADIUS, x+RADIUS, y+RADIUS, fill=self.fill, outline=self.outline, width=3,tags=tag)
	
	def project_on_boundary(self, x, y):
		x_0,y_0 = self.center
		norm = sqrt((x-x_0)**2 + (y-y_0)**2)
		
		return Waypoint(floor(self.radius*((x-x_0)/norm)+x_0), floor(self.radius*((y-y_0)/norm)+y_0), self)

class Handle:
	def __init__(self, circle_1, circle_2):
		self.circle_1 = circle_1
		self.circle_2 = circle_2
	
	def draw(self, canvas):
		self.circle_1.draw(canvas)
		self.circle_2.draw(canvas)
	
	def get_circle(self, click):
		nearby_objects = find_nearby(click, 2)
		for thing in nearby_objects:
			if thing == self.circle_1.picture:
				return self.circle_1
			elif thing == self.circle_2.picture:
				return self.circle_2
		return None
	
	def glued_point(self, circle, x, y):
		if circle == self.circle_1:
			identified_circle = self.circle_2
		elif circle == self.circle_2:
			identified_circle = self.circle_1
		else:
			raise RuntimeError('circle not part of handle')
		
		x_0,y_0 = circle.center
		x_1,y_1 = identified_circle.center
		return identified_circle.project_on_boundary(-(x-x_0)+x_1, y-y_0+y_1)

class Arc:
	def __init__(self, end_1, end_2):
		self.v1 = end_1
		self.v2 = end_2
		self.picture = None
		self.subarcs = []
	
	def draw(self, canvas, color='brown',in_diagram=False):
		if self.picture != None:
			canvas.delete(self.picture)
		
		if in_diagram:
			tag = 'in_diagram'
		else:
			tag='not_in_diagram'
		
		if self.subarcs == []:
			self.picture = canvas.create_line(*self.v1.coordinates(), *self.v2.coordinates(), width=4, fill=color,tags=tag)
			self.v1.draw(canvas)
			self.v2.draw(canvas)
		else:
			self.picture = None
			for arc in self.subarcs:
				arc.draw(canvas,color,in_diagram)
	
	def opposite_vertex(self, vertex):
		if self.v1 == vertex:
			return self.v1
		elif self.v2 == vertex:
			return self.v2
		else:
			raise RuntimeError('vertex is not an endpoint of arc')
	
	def add_waypoint(self, click):
		waypoint = Waypoint(click.x, click.y)
		self.subarcs = [Arc(self.v1,waypoint), Arc(waypoint,self.v2)]
		self.draw(click.widget)
	
	def subarc_with_picture(self, picture):
		if self.picture == picture:
			return self
		else:
			for subarc in self.subarcs:
				a = subarc.subarc_with_picture(picture)
				if a != None:
					return a
			return None
	
	def waypoints(self):
		waypoints = []
		for subarc in self.subarcs:
			waypoints += subarc.waypoints()
			if type(subarc.v1) == Waypoint and subarc.v1.circle != None:
				waypoints.append(subarc.v1)
			if type(subarc.v2) == Waypoint:
				waypoints.append(subarc.v2)
		return waypoints
	
	def cross(arc_1, arc_2):
		if arc_1.subarcs == []:
			if arc_2.subarcs == []:
				def f(x, y, x1, y1, x2, y2):
					return (x-x1)*(y2-y1)-(y-y1)*(x2-x1)
				
				arc_1_ends_on_opposite_sides_of_arc_2 = f(*arc_1.v1.coordinates(), *arc_2.v1.coordinates(), *arc_2.v2.coordinates())*f(*arc_1.v2.coordinates(), *arc_2.v1.coordinates(), *arc_2.v2.coordinates()) < 0
				arc_2_ends_on_opposite_sides_of_arc_1 = f(*arc_2.v1.coordinates(), *arc_1.v1.coordinates(), *arc_1.v2.coordinates())*f(*arc_2.v2.coordinates(), *arc_1.v1.coordinates(), *arc_1.v2.coordinates()) < 0
				
				return arc_1_ends_on_opposite_sides_of_arc_2 and arc_2_ends_on_opposite_sides_of_arc_1
			else:
				for subarc in arc_2.subarcs:
					if Arc.cross(arc_1,subarc):
						return True
				return False
		else:
			for subarc in arc_1.subarcs:
				if Arc.cross(subarc,arc_2):
					return True
			return False
	
	def extend(self, arc):
		initial_subarc = Arc(self.v1,self.v2)
		initial_subarc.subarcs = self.subarcs
		self.subarcs = [initial_subarc, arc]
		self.v2 = arc.v2
	
	def passes_through_handle(self):
		for waypoint in self.waypoints():
			if waypoint.circle != None:
				return True
		return False

class Diagram:
	def __init__(self):
		self.boundary_components = []
		self.handles = []
		self.arcs = []
	
	def add_arc(self, vertex_1, vertex_2):
		self.arcs.append(Arc(vertex_1, vertex_2))
	
	def draw(self, canvas):
		canvas.delete('all')
		
		if self.boundary_components != []:
			self.boundary_components[0].draw(canvas, "#c1e386")
			for boundary in self.boundary_components[1:]:
				boundary.draw(canvas)
		
		for arc in self.arcs:
			arc.draw(canvas,in_diagram=True)
		
		for handle in self.handles:
			handle.draw(canvas)
	
	def get_vertex(self, click):
		for picture_id in find_nearby(click):
			for boundary in self.boundary_components:
				for v in boundary.vertices:
					if v.picture == picture_id:
						return v
		return None
	
	def get_circle(self, click):
		for handle in self.handles:
			circle = handle.get_circle(click)
			if circle != None:
				return circle, handle
		return None, None
	
	def get_boundary_component(self, vertex):
		for component in self.boundary_components:
			if vertex in component.vertices:
				return component
		
		raise ValueError('vertex not in diagram')
	
	def trivial(self, arc):
		if arc.passes_through_handle():
			return False
		
		b = self.get_boundary_component(arc.v1)
		
		if b == self.get_boundary_component(arc.v2):
			i = b.vertices.index(arc.v1)
			j = b.vertices.index(arc.v2)
			if abs(i-j) <= 1 or abs(i-j) == len(b.vertices)-1:
				return True
		
		return False		
	
	def compatible(self, arc):
		if self.trivial(arc):
			return False
		
		for a in self.arcs:
			if Arc.cross(a, arc):
				return False
		
		return True
	
	def is_valid_vertex(self, vertex):
		if self.boundary_components == []:
			return True
		else:
			inside_outer_boundary = self.boundary_components[0].contains(*vertex.coordinates())
			outside_inner_boundaries = True
			for boundary in self.boundary_components[1:]:
				if boundary.contains(*vertex.coordinates()):
					outside_inner_boundaries = False
					break
			return inside_outer_boundary and outside_inner_boundaries
	
	def get_arc(self, click):
		for picture_id in click.widget.find_withtag('current'):
			for arc in self.arcs:
				a = arc.subarc_with_picture(picture_id)
				if a != None:
					return a
		return None
	
	def add_waypoint(self, click):
		a = self.get_arc(click)
		if a != None:
			a.add_waypoint(click)
	
	def get_waypoint(self, event):
		picture = get_picture_id(event)
		for arc in self.arcs:
			for waypoint in arc.waypoints():
				if waypoint.picture == picture:
					return waypoint
		return None
	
	def incident_arcs(self, vertex):
		arcs = []
		for arc in self.arcs:
			if arc.v1 == vertex or arc.v2 == vertex:
				arcs.append(arc)
		return arcs
	
	def order_arcs(self, vertex):
		boundary = self.get_boundary_component(vertex)
		is_outer_boundary = (self.boundary_components.index(boundary) == 0)
		
		if is_outer_boundary:
			
		
#-------------------GUI-------------------------------------------------

class Widgets:
	def __init__(self, parent, diagram):
		self.parent = parent
		self.diagram = diagram
		
		#large layout elements
		self.button_bar = tk.Frame(parent)
		self.button_bar.pack()
		
		self.canvas = tk.Canvas(width=640,height=480,background="white")
		self.canvas.pack(fill='both',expand=True)
		
		#buttons and controls
		self.new_diagram_button = tk.Button(self.button_bar, text="New diagram", command=self.new_diagram)
		self.new_boundary_button = tk.Button(self.button_bar, text="Add boundary component", command=self.add_boundary)
		self.new_handle_button = tk.Button(self.button_bar, text="Add handle", command=self.add_handle)
		self.move_boundary_button = tk.Button(self.button_bar, text="Move boundary vertices", command=self.move_boundary)
		self.add_arc_button = tk.Button(self.button_bar, text="Add arc", command=self.add_arc)
		self.waypoint_button = tk.Button(self.button_bar, text="Add/move waypoints", command=self.waypoint_tool)
		
		self.new_diagram_button.pack(side="left")
		self.new_boundary_button.pack(side="left")
		self.new_handle_button.pack(side="left")
		self.move_boundary_button.pack(side="left")
		self.add_arc_button.pack(side="left")
		self.waypoint_button.pack(side="left")
	
	#Button callbacks
	
	def unpress_all(self):
		for button in self.button_bar.winfo_children():
			button.config(relief="raised")
		
		self.canvas.unbind("<Button-1>")
		self.canvas.unbind("<Button-3>")
		self.canvas.unbind("<Double-Button-1>")
		self.canvas.unbind("<B1-Motion>")
		self.canvas.unbind("<ButtonRelease-1>")
		self.canvas.unbind("<Motion>")
		
		self.waypoint_button.config(command=self.waypoint_tool)
		self.move_boundary_button.config(command=self.move_boundary)
		self.add_arc_button.config(command=self.add_arc)
		self.new_handle_button.config(command=self.add_handle)
		
		self.diagram.draw(self.canvas)
	
	def new_diagram(self):
		self.unpress_all()
		self.diagram = Diagram()
		self.canvas.delete("all")
	
	def add_boundary(self):
		self.unpress_all()
		self.new_boundary_button.config(relief="sunken")
		
		vertices = []
		
		def make_vertex(click):
			if len(vertices)%2 == 0:
				v = Vertex(click.x, click.y, color='black')
			else:
				v = Vertex(click.x, click.y, color='red')
			
			if self.diagram.is_valid_vertex(v):
				v.draw(self.canvas)
				vertices.append(v)
		
		def finish(event):
			if len(vertices)>0 and len(vertices)%2==0:
				self.diagram.boundary_components.append(Boundary(*vertices))
			self.unpress_all()
		
		self.canvas.bind("<Button-1>", make_vertex)
		self.canvas.bind("<Double-Button-1>", finish)
	
	def add_arc(self):
		self.unpress_all()
		self.add_arc_button.config(relief="sunken",command=self.unpress_all)
		
		v = None
		
		new_arc = None
		
		def select(click):
			nonlocal v
			nonlocal new_arc
			
			if v == None:
				v = self.diagram.get_vertex(click)
				if v != None:
					v.draw(self.canvas,active=True,in_diagram=True)
			else:
				V = self.diagram.get_vertex(click)
				if V != None:
					if new_arc == None:
						new_arc = Arc(v,V)
					else:
						new_arc.extend(Arc(v,V))
					
					if self.diagram.compatible(new_arc):
						self.diagram.arcs.append(new_arc)
					self.unpress_all()
		
		def drag(event):
			if v != None:
				self.diagram.draw(self.canvas)
				if new_arc != None:
					new_arc.draw(self.canvas)
					
					if v != new_arc.v2:
						v.draw(self.canvas, active = True)
					
				self.canvas.create_line(*v.coordinates(), event.x, event.y)
		
		def add_waypoint(click):
			nonlocal v
			nonlocal new_arc
			
			if v != None:
				objects = find_nearby(click)
				circle, handle = self.diagram.get_circle(click)
				V = Waypoint(click.x, click.y, circle)
				
				if new_arc == None:
					new_arc = Arc(v, V)
				else:
					new_arc.extend(Arc(v,V))
				
				if circle == None:
					v = V
				else:
					v = handle.glued_point(circle, click.x, click.y)
				
				new_arc.draw(self.canvas)
				if v != new_arc.v2:
					v.draw(self.canvas, active = True)
		
		self.canvas.bind("<Button-1>", select)
		self.canvas.bind("<Motion>",drag)
		self.canvas.bind("<Button-3>", add_waypoint)
	
	def move_boundary(self):
		self.unpress_all()
		self.move_boundary_button.config(relief='sunken',command=self.unpress_all)
		
		active_vertex = None
		
		def select(click):
			nonlocal active_vertex
			active_vertex = self.diagram.get_vertex(click)
			if active_vertex != None:
				active_vertex.draw(self.canvas,active=True)
		
		def drag(event):
			if active_vertex != None:
				active_vertex.move(event)
				self.diagram.draw(self.canvas)
				active_vertex.draw(self.canvas, active=True)
		
		self.canvas.bind("<Button-1>",select)
		self.canvas.bind("<B1-Motion>",drag)
	
	def waypoint_tool(self):
		self.unpress_all()
		self.waypoint_button.config(relief='sunken',command=self.unpress_all)
		
		active_waypoint = None
		
		def select(click):
			nonlocal active_waypoint
			active_waypoint = self.diagram.get_waypoint(click)
			self.diagram.draw(self.canvas)
			if active_waypoint != None:
				active_waypoint.draw(self.canvas,active=True)
		
		def drag(event):
			if active_waypoint != None:
				if active_waypoint.circle == None:
					active_waypoint.x = event.x
					active_waypoint.y = event.y
				else:
					w = active_waypoint.circle.project_on_boundary(event.x, event.y)
					active_waypoint.x = w.x
					active_waypoint.y = w.y
				
				self.diagram.draw(self.canvas)
				active_waypoint.draw(self.canvas,active=True)
		
		self.canvas.bind("<Button-1>",select)
		self.canvas.bind("<B1-Motion>",drag)
		self.canvas.bind("<Button-3>",self.diagram.add_waypoint)
	
	def add_handle(self):
		self.new_handle_button.config(relief='sunken', command=self.unpress_all)
		
		circle = None
		x = 0
		y = 0
		radius = 0
		
		def click(event):
			nonlocal x,y
			x = event.x
			y = event.y
		
		def drag(event):
			nonlocal radius
			radius = floor(sqrt((event.x-x)**2+(event.y-y)**2))
			Circle((x,y), radius).draw(self.canvas)
		
		def release(event):
			nonlocal circle
			if circle == None:
				circle = Circle((x,y), radius)
			else:
				self.diagram.handles.append(Handle(circle, Circle((x,y), radius)))
				self.diagram.draw(self.canvas)
				self.unpress_all()
		
		self.canvas.bind('<Button-1>', click)
		self.canvas.bind('<B1-Motion>', drag)
		self.canvas.bind('<ButtonRelease-1>', release)
#--------------------------Misc utilities-------------------------------

def get_picture_id(event):
	return event.widget.find_withtag('current')[0]

def find_nearby(event, tolerance=3):
	x = event.x
	y = event.y
	return event.widget.find_overlapping(x-tolerance, y-tolerance, x+tolerance, y+tolerance)

def clear_artifacts(canvas):
	for item in canvas.find_all():
			if 'in_diagram' not in canvas.gettags(item):
				canvas.delete(item)

#----------------------------------------------------------------------

def main():
	root = tk.Tk()
	root.title("Arc Diagram Tools")
	
	widgets = Widgets(root,Diagram())
	
	root.mainloop()

# this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
