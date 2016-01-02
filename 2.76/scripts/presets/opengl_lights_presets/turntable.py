import bpy
l0 = bpy.context.user_preferences.system.solid_lights[0]
l1 = bpy.context.user_preferences.system.solid_lights[1]
l2 = bpy.context.user_preferences.system.solid_lights[2]

l0.use = True
l0.diffuse_color = (0.800000011920929, 0.6669999957084656, 0.6019999980926514)
l0.specular_color = (0.3280999958515167, 0.3280999958515167, 0.3280999958515167)
l0.direction = (0.0333000011742115, 0.2443999946117401, 0.968999981880188)
l1.use = False
l1.diffuse_color = (0.49619999527931213, 0.49619999527931213, 0.49619999527931213)
l1.specular_color = (0.0, 0.0, 0.0)
l1.direction = (0.11110000312328339, 0.08888000249862671, 0.989799976348877)
l2.use = False
l2.diffuse_color = (1.0, 0.9574000239372253, 0.9057999849319458)
l2.specular_color = (1.0, 1.0, 1.0)
l2.direction = (-0.51419997215271, 0.51419997215271, -0.6863999962806702)
