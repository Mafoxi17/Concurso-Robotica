import os
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from .models import Competencia, Categoria, AreaEvaluacion, Regla, asignacion_jurado, Robot, inscripcion_competencia
from django.urls import reverse
from django.db.models import Sum
import datetime


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from login.models import Usuario, TipoUsuario, Equipo, ParticipantesEquipos

from django.contrib import messages

# Create your views here.
class CrearCompetenciaView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'crearCompetencia.html', context)
    
    def post(self, request, *args, **kwargs):
        print("Entro")


class PruebaCompetenciaView(View):
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, 'pruebaCompetencia.html', context)
    
    def post(self, request, *args, **kwargs):
        nombre_competencia = request.POST.get('nombre_competencia')
        descripcion_competencia = request.POST.get('descripcion_competencia')
        lugar_competencia = request.POST.get('lugar_competencia')
        fecha_competencia = request.POST.get('fecha_Competencia')
        fecha_limite_inscripcion = request.POST.get('fecha_limite_inscripcion_Competencia')
        fecha_limite_actualizar = request.POST.get('fecha_limite_actualizar_inscripcion_Competencia')
        
        nueva_competencia = Competencia(
            NombreCompetencia=nombre_competencia,
            DescipcionCompetencia=descripcion_competencia,
            LugarCompetencia=lugar_competencia,
            FechaCompetencia=fecha_competencia,
            FechaLimiteInscripcion=fecha_limite_inscripcion,
            FechaLimiteActualizarDatos=fecha_limite_actualizar,
            EstadoCompetencia = "Creando"
        )
        nueva_competencia.save()
        
        # Guardar archivos temporalmente y luego leer su contenido binario
        banner1 = request.FILES.get('inputGroupFile01')

        banner2 = request.FILES.get('inputGroupFile02')

        banner3 = request.FILES.get('inputGroupFile03')


        nombre_banner_1 = "Banner_1"
        nombre_banner_2 = "Banner_2"
        nombre_banner_3 = "Banner_3"

        # Rutas para la organización de archivos
        ruta_competencia = f"static/img/{nueva_competencia.NombreCompetencia}/"

        # Obtener la extensión de la banner_1
        nombre, extension = os.path.splitext(banner1.name)
        nombre_banner_1_con_extension = f"{nombre_banner_1}{extension}"

        # Obtener la extensión de la banner_2
        nombre, extension = os.path.splitext(banner2.name)
        nombre_banner_2_con_extension = f"{nombre_banner_2}{extension}"

        # Obtener la extensión de la banner_3
        nombre, extension = os.path.splitext(banner3.name)
        nombre_banner_3_con_extension = f"{nombre_banner_3}{extension}"

        if banner1:
            ruta_archivo = f"{ruta_competencia}{nombre_banner_1_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(banner1.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nueva_competencia.banner1 = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nueva_competencia.save()

        if banner2:
            ruta_archivo = f"{ruta_competencia}{nombre_banner_2_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(banner2.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nueva_competencia.banner2 = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nueva_competencia.save()

        if banner3:
            ruta_archivo = f"{ruta_competencia}{nombre_banner_3_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(banner3.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nueva_competencia.banner3 = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nueva_competencia.save()



        nueva_competencia = Competencia.objects.latest('id')  # Obtener la última competencia creada
        competencia_id = nueva_competencia.id

        return redirect(reverse('competencia:agregar_categorias', kwargs={'competencia_id': competencia_id}))


class crearCategoriaView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')
        context = {
            'competencia_id': competencia_id,
        }
        return render(request, 'crearCategoria.html', context)
    
    def post(self, request, *args, **kwargs):
        nombre_categoria = request.POST.get('nombre_categoria')
        descripcion_categoria = request.POST.get('descripcion_categoria')

        competencia_id = kwargs['competencia_id']

        competencia = get_object_or_404(Competencia, id=competencia_id)
        
        nueva_categoria = Categoria(
            NombreCategoria=nombre_categoria,
            DescipcionCategoria=descripcion_categoria,
            competencia = competencia
        )
        nueva_categoria.save()

        nueva_categoria = Categoria.objects.latest('id')
        categoria_id = nueva_categoria.id

        # Obtén el ID de la competencia desde los argumentos de la URL
        competencia_id = kwargs['competencia_id']

        # Redirige a crear_RA_CategoriaView con ambos IDs en la URL
        return redirect(reverse('competencia:crear_RA_categoria', kwargs={'competencia_id': competencia_id, 'categoria_id': categoria_id}))


class agregar_CategoriaView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        categorias = Categoria.objects.filter(competencia=competencia)

        context = {
            'competencia_id': competencia_id,
            'nombre_competencia': competencia.NombreCompetencia,
            'descripcion_competencia': competencia.DescipcionCompetencia,
            'categorias': categorias,
        }
        return render(request, 'agregar_Categorias.html', context)
    
    def post(self, request, *args, **kwargs):
        print("Post de prueba")





class crear_RA_CategoriaView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')
        categoria_id = self.kwargs.get('categoria_id')

        categoria = get_object_or_404(Categoria, id=categoria_id)

        reglas = Regla.objects.filter(categoria=categoria)
        areas = AreaEvaluacion.objects.filter(categoria=categoria)

        context = {
            'competencia_id': competencia_id,
            'categoria_id': categoria_id,
            'nombre_categoria': categoria.NombreCategoria,
            'descripcion_categoria': categoria.DescipcionCategoria,
            'reglas': reglas,
            'areas': areas,
        }
        return render(request, 'crear_RA_Categoria.html', context)
    
    def post(self, request, *args, **kwargs):
        print("Post de prueba")




class crearReglaView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')
        categoria_id = self.kwargs.get('categoria_id')

        context = {
            'competencia_id': competencia_id,
            'categoria_id': categoria_id,
        }
        return render(request, 'crearRegla.html', context)
    
    def post(self, request, *args, **kwargs):

        nombre_regla = request.POST.get('nombre_regla')
        descripcion_regla = request.POST.get('descripcion_regla')

        competencia_id = self.kwargs.get('competencia_id')
        categoria_id = self.kwargs.get('categoria_id')

        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        nueva_regla = Regla(
            NombreRegla=nombre_regla,
            DescipcionRegla=descripcion_regla,
            categoria = categoria
        )
        nueva_regla.save()


        return redirect(reverse('competencia:crear_RA_categoria', kwargs={'competencia_id': competencia_id, 'categoria_id': categoria_id}))



class crearAreaEvaluacionView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')
        categoria_id = self.kwargs.get('categoria_id')

        context = {
            'competencia_id': competencia_id,
            'categoria_id': categoria_id,
        }
        return render(request, 'crearAreaEvaluacion.html', context)
    
    def post(self, request, *args, **kwargs):
        nombre_area_evaluacion = request.POST.get('nombre_area_evaluacion')
        descripcion_area_evaluacion = request.POST.get('descripcion_area_evaluacion')
        porcentaje_area_evaluacion = request.POST.get('porcentaje_area_evaluacion')

        competencia_id = self.kwargs.get('competencia_id')
        categoria_id = self.kwargs.get('categoria_id')

        categoria = get_object_or_404(Categoria, id=categoria_id)

        porcentaje_total = AreaEvaluacion.objects.filter(categoria=categoria).aggregate(total=Sum('Porcentaje'))['total'] or 0

        # Sumar el porcentaje del área de evaluación que se está intentando agregar
        nuevo_porcentaje = int(porcentaje_area_evaluacion)
        total_con_nuevo = porcentaje_total + nuevo_porcentaje

        # Validar si al agregar el nuevo porcentaje supera el 100%
        if total_con_nuevo > 100:
            messages.error(request, 'La suma de los porcentajes de las áreas de evaluación supera el 100%.')
            return redirect(reverse('competencia:crear_RA_categoria', kwargs={'competencia_id': competencia_id, 'categoria_id': categoria_id}))
            
        nueva_area_evaluacion = AreaEvaluacion(
            NombreAreaEvaluacion=nombre_area_evaluacion,
            DescipcionAreaEvaluacion=descripcion_area_evaluacion,
            Porcentaje=porcentaje_area_evaluacion,
            categoria = categoria
        )
        nueva_area_evaluacion.save()


        return redirect(reverse('competencia:crear_RA_categoria', kwargs={'competencia_id': competencia_id, 'categoria_id': categoria_id}))



class Mostrar_InformacionView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        categorias = Categoria.objects.filter(competencia=competencia)

        # Obtener las reglas y áreas de evaluación para cada categoría
        for categoria in categorias:
            categoria.reglas = Regla.objects.filter(categoria=categoria)
            categoria.areas_evaluacion = AreaEvaluacion.objects.filter(categoria=categoria)


        context = {
            'competencia_id': competencia_id,
            'competencia': competencia,
            'nombre_competencia': competencia.NombreCompetencia,
            'descripcion_competencia': competencia.DescipcionCompetencia,
            'categorias': categorias,
        }
        return render(request, 'Mostrar_Informacion.html', context)
    
    def post(self, request, *args, **kwargs):
        print("Post de prueba")



class ModificarCompetenciaView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        categorias = Categoria.objects.filter(competencia=competencia)

        # Obtener las reglas y áreas de evaluación para cada categoría
        for categoria in categorias:
            categoria.reglas = Regla.objects.filter(categoria=categoria)
            categoria.areas_evaluacion = AreaEvaluacion.objects.filter(categoria=categoria)


        context = {
            'competencia_id': competencia_id,
            'competencia': competencia,
            'nombre_competencia': competencia.NombreCompetencia,
            'descripcion_competencia': competencia.DescipcionCompetencia,
            'categorias': categorias,
        }
        return render(request, 'modificar_Competencia.html', context)
    
    def post(self, request, *args, **kwargs):
        print("Post de prueba")




class AsignarJurdoView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        asignaciones = asignacion_jurado.objects.select_related('area_evaluacion__categoria', 'usuario').filter(area_evaluacion__categoria__competencia=competencia)

        # Obtener categorías y áreas de evaluación con asignaciones
        categorias_con_asignaciones = {}
        for asignacion in asignaciones:
            categoria_id = asignacion.area_evaluacion.categoria.id
            area_evaluacion_id = asignacion.area_evaluacion.id

            if categoria_id not in categorias_con_asignaciones:
                categorias_con_asignaciones[categoria_id] = {'categoria': asignacion.area_evaluacion.categoria, 'areas_evaluacion': {}}

            if area_evaluacion_id not in categorias_con_asignaciones[categoria_id]['areas_evaluacion']:
                categorias_con_asignaciones[categoria_id]['areas_evaluacion'][area_evaluacion_id] = {
                    'area_evaluacion': asignacion.area_evaluacion,
                    'asignaciones': [asignacion.usuario],
                }
            else:
                categorias_con_asignaciones[categoria_id]['areas_evaluacion'][area_evaluacion_id]['asignaciones'].append(asignacion.usuario)
        

        categorias = Categoria.objects.filter(competencia=competencia)

        # Obtener las áreas de evaluación para cada categoría
        for categoria in categorias:
            categoria.areas_evaluacion = AreaEvaluacion.objects.filter(categoria=categoria)
        

        
        context = {
            'competencia_id': competencia_id,
            'competencia': competencia,
            'categorias': categorias,
            'categorias_con_asignaciones': categorias_con_asignaciones,
        }
        return render(request, 'AsignarJurado.html', context)
    
    def post(self, request, *args, **kwargs):

        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        categorias = Categoria.objects.filter(competencia=competencia)

        # Obtener las áreas de evaluación para cada categoría
        for categoria in categorias:
            categoria.areas_evaluacion = AreaEvaluacion.objects.filter(categoria=categoria)
        

        categoria_seleccionada = request.POST.get('categoria_seleccionada')
        AreasEvaluacion_seleccionada = request.POST.get('AreasEvaluacion_seleccionada')
        busqueda = request.POST.get('busqueda')

        # Realizar la búsqueda del usuario en la base de datos
        try:
            usuario = Usuario.objects.get(Nombre1=busqueda)  # Modifica esto según tus campos de usuario
            area_evaluacion = get_object_or_404(AreaEvaluacion, id=AreasEvaluacion_seleccionada)
            
            tipo_usuario = get_object_or_404(TipoUsuario, NombreTipoUsuario="Jurado")

            usuario.tipo_usuario = tipo_usuario
            usuario.save()

            nueva_asignacion = asignacion_jurado(
                usuario = usuario,
                area_evaluacion = area_evaluacion,
            )
            nueva_asignacion.save()
            
        except Usuario.DoesNotExist:
            # Si no se encuentra, muestra un mensaje de error utilizando Django messages framework
            messages.error(request, 'El usuario no se encontró en la base de datos.')

        # Devuelve la página, incluyendo los datos y mensajes actualizados
        return redirect(reverse('competencia:asignar_jurado', kwargs={'competencia_id': competencia_id}))


class Inscripcion_ExitosaView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        context = {
            'competencia_id': competencia_id,
            'competencia': competencia,
        }
        return render(request, 'confirmacion_Inscripcion.html', context)



def buscar_usuario_por_correo(correo):
    try:
        usuario = Usuario.objects.get(correo=correo)
        return usuario
    except Usuario.DoesNotExist:
        return None



class InscripcionCompetenciaView(View):
    def get(self, request, *args, **kwargs):
        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        categorias = Categoria.objects.filter(competencia=competencia)

        context = {
            'competencia': competencia,
            'categorias': categorias,
        }
        return render(request, 'InscripcionCompetencia.html', context)
    
    def post(self, request, *args, **kwargs):

        competencia_id = self.kwargs.get('competencia_id')

        competencia = get_object_or_404(Competencia, id=competencia_id)

        categorias = Categoria.objects.filter(competencia=competencia)
        

        categoria_seleccionada = request.POST.get('categoria_seleccionada')

        nombre_equipo = request.POST.get('nombre_equipo')
        color_equipo = request.POST.get('color_equipo')
        descripcion_equipo = request.POST.get('descripcion_equipo')
        integrante_1 = request.POST.get('integrante_1')
        integrante_2 = request.POST.get('integrante_2')
        integrante_3 = request.POST.get('integrante_3')
        imagen_equipo = request.FILES.get('imagen_equipo')
        video_equipo = request.FILES.get('video_equipo')

        nombre_robot = request.POST.get('nombre_robot')
        descripcion_robot = request.POST.get('descripcion_robot')
        imagen_robot = request.FILES.get('imagen_robot')
        diagrama_conexiones = request.FILES.get('diagrama_conexiones')
        programacion_robot = request.FILES.get('programacion_robot')

        imagen_aplicacion = request.FILES.get('imagen_aplicacion')
        
        if categoria_seleccionada== "Seleccionar...":
            messages.error(request, 'Por favor seleccione una categoria.')
            context = {
                'competencia': competencia,
                'categorias': categorias,
            }
            return render(request, 'InscripcionCompetencia.html', context)
        

        if not nombre_equipo or not color_equipo or not descripcion_equipo or not integrante_1 or not imagen_equipo or not video_equipo or not nombre_robot or not descripcion_robot or not imagen_robot or not diagrama_conexiones or not programacion_robot or not imagen_aplicacion:
            messages.error(request, 'Por favor ingrese todos los capos que tienen (*).')
            context = {
                'competencia': competencia,
                'categorias': categorias,
            }
            return render(request, 'InscripcionCompetencia.html', context)
        
        fecha_actual = datetime.date.today()
        if fecha_actual > competencia.FechaLimiteInscripcion:
            messages.error(request, 'La fecha límite de inscripción ha expirado.')
            context = {
                'competencia': competencia,
                'categorias': categorias,
            }
            return render(request, 'InscripcionCompetencia.html', context)

        
        categoria = get_object_or_404(Categoria, id=categoria_seleccionada)

        correos_integrantes = [integrante_1, integrante_2, integrante_3]

        usuarios_encontrados = []

        for correo in correos_integrantes:
            if correo != '':
                usuario = buscar_usuario_por_correo(correo)
                if usuario:
                    usuarios_encontrados.append(usuario)
                else:
                    messages.error(request, f'No se encontró al usuario con el correo: {correo}')
                    context = {
                        'competencia': competencia,
                        'categorias': categorias,
                    }
                    return render(request, 'InscripcionCompetencia.html', context)
        
        nuevo_equipo = Equipo(
            NombreEquipo = nombre_equipo,
            DescipcionEquipo = descripcion_equipo,
        )
        nuevo_equipo.save()

        nombre_imagen_equipo = "Imagen_equipo"
        nombre_video_equipo = "Video_equipo"

        # Obtener la extensión de la imagen_equipo
        nombre, extension = os.path.splitext(imagen_equipo.name)
        nombre_imagen_equipo_con_extension = f"{nombre_imagen_equipo}{extension}"

        # Obtener la extensión de la video_equipo
        nombre, extension = os.path.splitext(video_equipo.name)
        nombre_video_equipo_con_extension = f"{nombre_video_equipo}{extension}"

        # Rutas para la organización de archivos
        ruta_competencia = f"static/img/{competencia.NombreCompetencia}/"
        ruta_categoria = f"{ruta_competencia}/{categoria.NombreCategoria}/"
        ruta_equipo = f"{ruta_categoria}/{nuevo_equipo.id}_{nombre_equipo}/"

    
        if imagen_equipo:
            ruta_archivo = f"{ruta_equipo}{nombre_imagen_equipo_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(imagen_equipo.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nuevo_equipo.imagen_equipo = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nuevo_equipo.save()
    
        if video_equipo:
            ruta_archivo = f"{ruta_equipo}{nombre_video_equipo_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(video_equipo.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nuevo_equipo.video_equipo = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nuevo_equipo.save()
        
        for usuario in usuarios_encontrados:
            # Verificar si el usuario ya tiene una relación "activa" con otro equipo
            if ParticipantesEquipos.objects.filter(usuario=usuario, Estado_ParticipanteEquipo="Activo").exists():
                mensaje_error = f"El usuario {usuario} ya tiene una relación activa con otro equipo."
                messages.error(request, mensaje_error)
                context = {
                    'competencia': competencia,
                    'categorias': categorias,
                }
                return render(request, 'InscripcionCompetencia.html', context)
            else:
                # Si el usuario no tiene una relación activa, crear la nueva relación
                nueva_participacion = ParticipantesEquipos(
                    usuario=usuario,
                    equipo=nuevo_equipo
                )
                nueva_participacion.save()
        
        nuevo_robot = Robot(
            NombreRobot = nombre_robot,
            DescripcionRobot = descripcion_robot,
        )
        nuevo_robot.save()

        nombre_imagen_robot = "Imagen_robot"
        nombre_diagrama_conexiones = "Diagrama_conexiones"
        nombre_programacion_robot = "Programacion_robot"

        # Obtener la extensión de la imagen_robot
        nombre, extension = os.path.splitext(imagen_robot.name)
        nombre_imagen_robot_con_extension = f"{nombre_imagen_robot}{extension}"

        # Obtener la extensión de la diagrama_conexiones
        nombre, extension = os.path.splitext(diagrama_conexiones.name)
        nombre_diagrama_conexiones_con_extension = f"{nombre_diagrama_conexiones}{extension}"

        # Obtener la extensión de la programacion_robot
        nombre, extension = os.path.splitext(programacion_robot.name)
        nombre_programacion_robot_con_extension = f"{nombre_programacion_robot}{extension}"

        if imagen_robot:
            ruta_archivo = f"{ruta_equipo}Robot/{nombre_imagen_robot_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(imagen_robot.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nuevo_robot.imagen_robot = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nuevo_robot.save()

        if diagrama_conexiones:
            ruta_archivo = f"{ruta_equipo}Robot/{nombre_diagrama_conexiones_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(diagrama_conexiones.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nuevo_robot.diagrama_conexiones = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nuevo_robot.save()

        if programacion_robot:
            ruta_archivo = f"{ruta_equipo}Robot/{nombre_programacion_robot_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(programacion_robot.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nuevo_robot.programacion_robot = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nuevo_robot.save()
        
        nueva_inscripcion = inscripcion_competencia(
            color = color_equipo,
            categoria = categoria,
            equipo = nuevo_equipo,
            robot = nuevo_robot
        )
        nueva_inscripcion.save()

        nombre_imagen_aplicacion = "Imagen_aplicacion"

        # Obtener la extensión de la programacion_robot
        nombre, extension = os.path.splitext(imagen_aplicacion.name)
        nombre_imagen_aplicacion_con_extension = f"{nombre_imagen_aplicacion}{extension}"

        if imagen_aplicacion:
            ruta_archivo = f"{ruta_equipo}{nombre_imagen_aplicacion_con_extension}"
            ruta_archivo_temporal = default_storage.save(ruta_archivo, ContentFile(imagen_aplicacion.read()))

            # Actualizar el modelo Equipo con la ruta del archivo
            nueva_inscripcion.imagen_aplicacion = ruta_archivo  # Asigna la ruta al campo correspondiente en el modelo
            nueva_inscripcion.save()
        
        competencia_id = competencia.id
        
        return redirect(reverse('competencia:incripcion_exitosa', kwargs={'competencia_id': competencia_id}))


class Mostrar_InformacionCompetenciaView(View):
    def get(self, request, *args, **kwargs):
        competencias = Competencia.objects.filter(EstadoCompetencia="Disponible")
        
        competencias_info = []
        for competencia in competencias:
            categorias = Categoria.objects.filter(competencia=competencia)
            for categoria in categorias:
                categoria.reglas = Regla.objects.filter(categoria=categoria)
                categoria.areas_evaluacion = AreaEvaluacion.objects.filter(categoria=categoria)

            competencias_info.append({
                'competencia': competencia,
                'categorias': categorias
            })

        context = {
            'competencias_info': competencias_info,
        }
        return render(request, 'mostrar_competencias.html', context)


class GestionarCompetenciasView(View):
    def get(self, request, *args, **kwargs):
        competencias = Competencia.objects.filter(EstadoCompetencia="Disponible")
        
        competencias_info = []
        for competencia in competencias:
            categorias = Categoria.objects.filter(competencia=competencia)
            for categoria in categorias:
                categoria.reglas = Regla.objects.filter(categoria=categoria)
                categoria.areas_evaluacion = AreaEvaluacion.objects.filter(categoria=categoria)

            competencias_info.append({
                'competencia': competencia,
                'categorias': categorias
            })

        context = {
            'competencias_info': competencias_info,
        }
        return render(request, 'Gestionar_Competencias.html', context)