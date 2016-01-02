import bpy
l0 = bpy.context.user_preferences.system.solid_lights[0]
l1 = bpy.context.user_preferences.system.solid_lights[1]
l2 = bpy.context.user_preferences.system.solid_lights[2]

l0.use = True
l0.diffuse_color = (0.6618000268936157, 0.5480999946594238, 0.5054000020027161)
l0.specular_color = (0.4968999922275543, 0.4885999858379364, 0.4819999933242798)
l0.direction = (0.36660000681877136, 0.2888000011444092, 0.8842999935150146)
l1.use = True
l1.diffuse_color = (0.36719998717308044, 0.2371000051498413, 0.17520000040531158)
l1.specular_color = (0.0, 0.0, 0.0)
l1.direction = (0.11110000312328339, 0.08879999816417694, 0.989799976348877)
l2.use = True
l2.diffuse_color = (1.0, 0.9574000239372253, 0.9057999849319458)
l2.specular_color = (1.0, 1.0, 1.0)
l2.direction = (-0.51419997215271, 0.51419997215271, -0.6863999962806702)
