from django.views.decorators.csrf import csrf_exempt
from .utils import create_connection, Consulta, Categoria, Curso, fetch_data_to_dataframe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import DatabaseConnectionForm
from .models import DatabaseConnection



@csrf_exempt
def setup_connection(request):
    if request.method == 'POST':
        form = DatabaseConnectionForm(request.POST)
        if form.is_valid():
            objConnection = form.save()
            return redirect('Consulta')
    else:
        form = DatabaseConnectionForm()
    return render(request, 'appTiindux/setup_connection.html', {'form': form})


@csrf_exempt
def select_query(request):
    objConnection = DatabaseConnection.objects.last()
    connection = create_connection(objConnection.host, objConnection.user, objConnection.password, objConnection.database)
    consulta = Consulta(Categoria(connection), Curso(connection))

    if request.method == 'GET':
        _, categorias_list = consulta.contar_categorias()
        category_name = categorias_list[0]
        query = f"SELECT * FROM mdl_course_categories WHERE idnumber = '{category_name}'"
        df_cat = fetch_data_to_dataframe(connection, query)
        _, cursos_list = consulta.contar_cursos_en_categoria(df_cat['id'][0])
        return render(request, 'appTiindux/select_query.html', {
            'categorias': categorias_list,
            'cursos': cursos_list
        })
    
    elif request.method == 'POST':
        category_name = request.POST.get('categoria_id')
        query = f"SELECT * FROM mdl_course_categories WHERE idnumber = '{category_name}'"
        df_cat = fetch_data_to_dataframe(connection, query)
        _, cursos_list = consulta.contar_cursos_en_categoria(df_cat['id'][0])
        return JsonResponse({'cursos': cursos_list})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def usuarios_por_curso(request):
    if request.method == 'POST':
        curso_name = request.POST.get('curso_id')
        objConnection = DatabaseConnection.objects.last()
        connection = create_connection(objConnection.host, objConnection.user, objConnection.password, objConnection.database)
        query_id = f"""
        SELECT id
        FROM mdl_course
        WHERE fullname = '{curso_name}'
        """
        id = fetch_data_to_dataframe(connection, query_id)['id'][0]
        print(id)
        # Consulta para obtener los usuarios que completaron el curso
        query = f"""
        SELECT u.id, u.firstname, u.lastname
        FROM mdl_course_completions cc
        JOIN mdl_user u ON cc.userid = u.id
        WHERE cc.course = '{id}'
        """
        try:
            df_users = fetch_data_to_dataframe(connection, query)
            usuarios_list = df_users.apply(lambda row: {
                'id': row['id'],
                'nombre': f"{row['firstname'].capitalize()} {row['lastname'].capitalize()}"
            }, axis=1).tolist()
        except Exception as e:
            usuarios_list = []
            
        return JsonResponse({'usuarios': usuarios_list})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)