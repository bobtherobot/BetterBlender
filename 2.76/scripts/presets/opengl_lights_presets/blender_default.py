import bpy
l0 = bpy.context.user_preferences.system.solid_lights[0]
l1 = bpy.context.user_preferences.system.solid_lights[1]
l2 = bpy.context.user_preferences.system.solid_lights[2]

l0.use = True
l0.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929)
l0.specular_color = (0.5, 0.5, 0.5)
l0.direction = (-0.8920000791549683, 0.30000001192092896, 0.8999999761581421)
l1.use = True
l1.diffuse_color = (0.4980020225048065, 0.500000536441803, 0.6000001430511475)
l1.specular_color = (0.20000000298023224, 0.20000000298023224, 0.20000000298023224)
l1.direction = (0.5880000591278076, 0.46000003814697266, 0.24800002574920654)
l2.use = True
l2.diffuse_color = (0.7980005145072937, 0.8379999399185181, 1.0)
l2.specular_color = (0.06599999219179153, 0.0, 0.0)
l2.direction = (0.21599984169006348, -0.3920000195503235, -0.21599996089935303)
