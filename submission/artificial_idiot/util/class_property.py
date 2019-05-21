class classproperty(property):
    """
    Class property decorator. Attribution to Aaron Hall♦ in
    https://stackoverflow.com/questions/128573/using-property-on-classmethods
    """
    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))
