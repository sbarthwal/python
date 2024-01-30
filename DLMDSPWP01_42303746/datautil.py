from sqlalchemy import create_engine, Float, MetaData, Table, Column, String


def write_results_to_db(result):
    """
    Method to write in DB
    :param result: save result dic
    """
    #DB setup
    engine = create_engine('sqlite:///{}.db'.format("output/mapping"), echo=True)
    metadata = MetaData()

    mapping = Table('mapping', metadata,
                    Column('TestFun_X', Float, primary_key=False),
                    Column('TestFun_Y', Float),
                    Column('TestFun_Delta_Y', Float),
                    Column('Ideal_Func_No', String(50))
                    )

    metadata.create_all(engine)



    resultsOPList = []
    for item in result:
        point = item["point"]
        classification = item["classification"]
        delta_y = item["delta_y"]


        classification_name = None
        if classification is not None:
            classification_name = classification.name.replace("y", "N")
        else:
            # EMPTY classification
            classification_name = "-"
            delta_y = -1

        resultsOPList.append(
            {"TestFun_X": point["x"], "TestFun_Y": point["y"], "TestFun_Delta_Y": delta_y,
             "Ideal_Func_No": classification_name})

    # insert data
    i = mapping.insert().values(resultsOPList)
    with engine.connect() as connection:
        connection.execute(i.compile(connection))
        connection.commit()

