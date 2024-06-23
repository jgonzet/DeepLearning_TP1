cols_df_movies = ["id", "Name", "Release Date", "IMDB URL", "unknown", "Action","Adventure","Animation", "Children's", "Comedy", "Crime","Documentary", "Drama", "Fantasy", "Film-Noir","Horror", "Musical","Mystery", "Romance","Sci-Fi", "Thriller", "War", "Western"]
pos_gens = 4

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

def get_year_from_df(date):
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
    def get_stats(cls, df_mov, anios=None, generos=None):
        # Este class method imprime una serie de estadísticas calculadas sobre
        # los resultados de una consulta al DataFrame df_mov. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # anios: [desde_año, hasta_año]
        # generos: [generos]
        # Las estadísticas son:
        # - Datos película más vieja
        # - Datos película más nueva
        # - Bar plots con la cantidad de películas por año/género.
        # if anios:
        #     desde_año, hasta_año = anios
        #     df_mov = df_mov[(df_mov['año'] >= desde_año) & (df_mov['año'] <= hasta_año)]
        # if generos:
        #     df_mov = df_mov[df_mov['género'].isin(generos)]
        anitos, generitos = anios, generos
        movies_selected = cls.get_from_df(df_mov, anios = anitos, generos = generitos)
        print(movies_selected)

        # pelicula_mas_vieja = df_mov.loc[df_mov['año'].idxmin()]
        # print("Película más vieja:")
        # print(pelicula_mas_vieja)
        
        # pelicula_mas_nueva = df_mov.loc[df_mov['año'].idxmax()]
        # print("\nPelícula más nueva:")
        # print(pelicula_mas_nueva)
        
        # plt.figure(figsize=(10, 6))
        # df_mov['año'].value_counts().sort_index().plot(kind='bar')
        # plt.title('Cantidad de películas por año')
        # plt.xlabel('Año')
        # plt.ylabel('Cantidad de películas')
        # plt.show()
        
        # plt.figure(figsize=(10, 6))
        # df_mov['género'].value_counts().plot(kind='bar')
        # plt.title('Cantidad de películas por género')
        # plt.xlabel('Género')
        # plt.ylabel('Cantidad de películas')
        # plt.show()
