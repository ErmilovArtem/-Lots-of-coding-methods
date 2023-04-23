def codeste(stres):
    type_of_stres = type(stres)
    stre = stres + type_of_stres([stres[0]])
    returned = type_of_stres()
    i = 0
    counter_of_ne = 0
    while i < len(stre) - 1:
        counter = i + 1
        while stre[counter] == stre[i] and counter - i < 7:
            counter += 1
        if counter - i > 1:
            if counter_of_ne > 0:
                if type_of_stres == str:
                    returned += type_of_stres(counter_of_ne) + stre[i - counter_of_ne:i]
                else:
                    returned += (str(counter_of_ne) + stre[i - counter_of_ne:i].decode("utf8")).encode("utf8")

            if type_of_stres == str:
                returned += type_of_stres(chr(ord("A") + (counter - i) - 2)) + stre[i]
            else:
                returned += (str(chr(ord("A") + (counter - i) - 2)) + bytes([stre[i]]).decode("utf8")).encode("utf8")
            counter_of_ne = 0
        else:
            counter_of_ne += 1
        i = counter
        if (i == len(stre) - 1) or (counter_of_ne > 6):
            if counter_of_ne > 0:
                if type_of_stres == str:
                    returned += type_of_stres(counter_of_ne) + stres[i - counter_of_ne:i]
                else:
                    returned += (str(counter_of_ne) + stre[i - counter_of_ne:i].decode("utf8")).encode("utf8")
            counter_of_ne = 0
    return returned

def decodeste(stre):
    type_of_stres = type(stre)
    returned = type_of_stres()
    stres = stre
    while len(stres) != 0:
        inted = stres[0]
        try:
            if type_of_stres == str:
                inted = int(type_of_stres(inted)) + 1
            if type_of_stres == bytes:
                inted = int(type_of_stres([inted])) + 1
            returned += stres[1:inted]
            stres = stres[inted:]
        except Exception:
            if type_of_stres == str:
                inted = ord(stres[0]) - 63
                returned += type_of_stres(stres[1]) * inted
            if type_of_stres == bytes:
                inted = ord((type_of_stres([stres[0]])).decode("utf8")) - 63
                returned += type_of_stres([stres[1]]) * inted
            stres = stres[2:]
    return returned

