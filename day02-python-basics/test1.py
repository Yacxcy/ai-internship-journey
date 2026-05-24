def fn_outer():
     a= 100
     def fn_inner():
          print(f"a:{a}")
     return fn_inner
if __name__ == "__main__":
     fn_inner=fn_outer()
     fn_inner()
     fn_inner()
     fn_inner()