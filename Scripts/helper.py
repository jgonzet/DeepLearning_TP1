cols_df_movies = ["id", "Name", "Release Date", "IMDB URL", "unknown", "Action","Adventure","Animation", "Children's", "Comedy", "Crime","Documentary", "Drama", "Fantasy", "Film-Noir","Horror", "Musical","Mystery", "Romance","Sci-Fi", "Thriller", "War", "Western"]
pos_gens = 4

cols_df_users = ["id","Occupation","Active Since"]
cols_df_pple = ["id","Full Name","year of birth","Gender","Zip Code"]

def get_gens():
    return cols_df_movies[pos_gens:]

def parse_movie(pelicula, df_movies):
    new_row = [pelicula.id,pelicula.nombre,"01-Jan-"+str(pelicula.anio),"unkown URL"]
    if len(pelicula.generos) == 0: new_row.append(1)
    else: new_row.append(0)
    for gen in df_movies.columns.tolist()[5:]:
        if gen in pelicula.generos: new_row.append(1)
        else: new_row.append(0)
    return new_row

def get_movies_structure():
    return cols_df_movies

def get_users_structure():
    return cols_df_users

def get_pple_structure():
    return cols_df_pple

def get_year_from_df(date):
    return int(date[-4:])

def get_date_from_df(date):
    return int(date[-4:])

def get_df_from_df(df_mov,id=None,nombre=None,anios=None,generos=None):
    mask = df_mov.copy()
    if id is not None:
        mask = mask[mask['id'] == id]
    if nombre is not None:
        mask = mask[mask['Name'].str.contains(nombre)]
    if anios is not None:
        mask = mask[(mask["Release Date"].apply(get_year_from_df)>= anios[0]) & (mask['Release Date'].apply(get_year_from_df) <= anios[1])]
    if generos is not None:
        for genero in generos:
            mask = mask[mask[f'{genero}'] == 1]
    return mask

def gen_from_one_hot(serie):
    serie_aux = serie[cols_df_movies[pos_gens:]]
    return serie_aux.index[serie_aux==1].tolist()




    @classmethod
    def get_from_df(cls, df_usr, id = None, ocupaciones=None , fechas=None):
        # Este class method devuelve una lista de objetos 'Usuario' buscando por:
        # id, nombre, anios: [desde_fecha, hasta_fecha], ocupacion: [ocupaciones]
        if fechas is not None:
            fechas_dt = list ( map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),fechas))
            mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones,fechas=fechas_dt)
        else: mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones)        
        usuarios = []
        for index, row in mask.iterrows():
            user = cls(id=row['id'], ocupacion = row["Occupation"], fecha_alta=row['Active Since'])
            usuarios.append(user)        
        return usuarios
    
    @classmethod
    def df_filter(cls,df_usr, id=None, fechas=None,ocupaciones=None):
        mask = df_usr.copy()
        if id is not None:
            mask = mask[mask['id'] == id]
        if fechas is not None:
            mask = mask[(mask['Active Since'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))>= fechas[0]) & (mask['Active Since'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S')) <= fechas[1])]        
        if ocupaciones is not None:
            mask = mask[mask['Occupation'].isin(ocupaciones)]
        return mask

    @classmethod
    def get_stats(cls, df_usr, fechas=None, ocupaciones=None):
        # Este class method imprime una serie de estadísticas calculadas sobre los resultados de una consulta al DataFrame df_usr. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # fechas: [desde_fecha, hasta_fecha]
        # ocupacion: [ocupaciones]
        # Las estadísticas son:
        # - Datos usuario más viejo
        # - Datos usuario más nuevo
        # - Bar plots con la cantidad de usuarios por anio/ocupacion.
        if fechas is not None:
            fechas_dt = list ( map(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),fechas))            
            mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones,fechas=fechas_dt)
        else: mask = Usuario.df_filter(df_usr,ocupaciones=ocupaciones)

        mask["Active Since"] = mask["Active Since"].apply(lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
        mask = mask.reset_index(drop=True)

        # user mas viejo
        row = mask.iloc[mask["Active Since"].idxmin()]
        print("Usuario más viejo: ")
        older_user = cls(id=row['id'], ocupacion=row["Occupation"], fecha_alta=row["Active Since"])
        print(older_user)        
        # user mas nuevo
        row = mask.iloc[mask["Active Since"].idxmax()]
        print("Usuario más nuevo: ")
        last_user = cls(id=row['id'], ocupacion=row["Occupation"], fecha_alta=row["Active Since"])
        print(last_user)    
        #grafico de generos
        conteo = mask['Occupation'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de usuarios por Ocupacion')
        plt.xlabel('Ocupaciones')
        plt.ylabel('Cantidad de Usuarios')
        plt.show()

        #grafico de anios
        mask["anio"] = mask["Active Since"].apply(lambda x: x.year)
        conteo = mask['anio'].value_counts()
        plt.figure(figsize=(10, 6))
        conteo.plot(kind='bar')
        plt.title('Cantidad de usuarios por año')
        plt.xlabel('Año')
        plt.ylabel('Cantidad de Usuarios')
        plt.show()