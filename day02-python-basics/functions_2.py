def greeting (name, greeting = "hello" , *args, **kwargs):
    print(f"{greeting}, {name}!")
    print("args:", args,"kwargs:", kwargs)

greeting("Ya","hi",1,2,3, age = 30)