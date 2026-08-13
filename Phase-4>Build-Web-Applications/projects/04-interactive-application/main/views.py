from django.shortcuts import redirect, render

def feedback(request):
    errors=[]
    values={"name":"","email":"","feedback":"","rating":""}
    if request.method == "POST":
        values={key: request.POST.get(key, "").strip() for key in values}
        if not values["name"]: errors.append("Name is required.")
        if not values["email"]: errors.append("Email is required.")
        if not values["feedback"]: errors.append("Feedback is required.")
        if values["rating"] not in {"1","2","3","4","5"}: errors.append("Choose a rating from 1 to 5.")
        if not errors:
            return render(request,"main/success.html",{"values":values})
    return render(request,"main/feedback.html",{"errors":errors,"values":values})
