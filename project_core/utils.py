from django.forms.utils import ErrorList


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return f"""
                <div class="text-sm text-danger">
                      {''.join(['<p>%s</p>' % e for e in self])}
                </div>
         """