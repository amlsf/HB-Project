import model

def load_master(session):
    f = open("seed_data/u.master")
    rows = f.read().split("\n")
    f.close()

    for line in rows:
        row = line.split("|")
        name = row[0]
        email = row[1]
        phone_num = row[2]
        full_address = row[3]
        lat = row[4]
        lng = row[5]
        supply_type = row[6]
        extra_comment = row[7]

        master = model.Master(name=name, email=email, phone_num=phone_num, full_address=full_address, lat=lat, lng=lng, supply_type=supply_type, extra_comment=extra_comment)
        user = model.User(name=name, email=email, phone_num=phone_num)
        location = model.Location(full_address=full_address, lat=lat, lng=lng)
        supply = model.Supply(supply_type=supply_type)
        comment = model.Comment(extra_comment=extra_comment)

        model.session.add(master)
        model.session.add(user)
        model.session.add(location)
        model.session.add(supply)
        model.session.add(comment)

def main(session):
    load_master(session)
    model.session.commit()

if __name__ == "__main__":
    s = model.connect()
    main(s)