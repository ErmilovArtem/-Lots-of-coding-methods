from colorama import Fore


def beauty_dict_print(dict, message="-_"):
    import json
    print(Fore.GREEN + ("\n" + "-_" * 13 + '(' + message + ')' + "-_" * 13 + "\n"
                        + json.dumps(dict, indent=4)[2:-2]
                        + "\n" + "-_" * (27 + int((len(message) / 2)))) + Style.RESET_ALL)


def beauty_list_print(list, message="-_"):
    print(Fore.CYAN + ("\n" + "-_" * 13 + '(' + message + ')' + "-_" * 13 + "\n"
                       + str(list).replace("', b'", "\n    ")
                       .replace("[b'", "    ").replace("']", "")
                       + "\n" + "-_" * (27 + int((len(message) / 2)))) + Style.RESET_ALL)