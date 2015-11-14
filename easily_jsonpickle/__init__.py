"""
Utilities to enhance the jsonpickle package.

DOESNT'T WORK WITH MULTIPLE REFERENCES TO OBJECTS.
Will create a new object each time instead of putting a reference.
That's because it was written to have manual control over these kinds of
things.
As a result, cyclic references will lead to infinite recursion.
A way to circumvent this is to implement reference handling yourself in your
object's flatten and restore methods.
I want to provide some utility functions to this end in the future.
"""

import jsonpickle
import jsonpickle.handlers

pickler = jsonpickle.pickler.Pickler()
unpickler = jsonpickle.unpickler.Unpickler()

def easily_to_json(
flatten_method_name, restore_method_name,
flatten_normally=[]
):
  """
  Returns a decorator which sets jsonpickle flatten and restore methods.

  :param str flatten_method_name: Name of the method that will be called in
  order to flatten the object.
  :param str restore_method_name: Name of the method that will be called in
  order to restore the object.
  :param flatten_normally: Attributes that should be flattened the way
  jsonpickle would normally do it. This happens before the method referred to
  by ``flatten_method_name`` is called, so you can make adjustments if you
  wish.
  :type flatten_normally: List of strings.

  The method referred to by ``flatten_method_name`` should be an *instance
  method* of the decorated class. It should be of the form ``f(self, data)``,
  ``data`` being a (partially filled) dictionary, namely the JSON-friendly
  representation of the object. You should fill this dictionary with anything
  else you need. The return value is ignored.

  The method referred to by ``restore_method_name``, in contrast, should be a
  *class method* of the decorated class, because you will want to create a new
  instance of the class inside this method. It should be of the form ``f(cls,
  data)``, data being the JSON-friendly representation of the object again,
  this time completely determined by jsonpickle. You should construct an
  instance of the class from this information and return it.

  Note that there can be no ``restore_normally`` because how would that work?
  Just think about it m8.
  """
  def easily_decorated(cls):
    """
    The actual decorator returned by ``easily_to_json``.
    """
    class EasyHandler(jsonpickle.handlers.BaseHandler):
      """
      jsonpickle Handler created by easily_decorated.
      """
      def flatten(self, obj, data):
        # Get flatten method associated with object.
        flatten_method = getattr(obj, flatten_method_name)
        # Flatten attributes declared normal first.
        for attr_name in flatten_normally:
          encoded = pickler.flatten(getattr(obj, attr_name), reset=False)
          data[attr_name] = encoded
        # Now for the user's flatten method.
        flatten_method(data)
        return data
      def restore(self, data):
        # Get restore method associated with class.
        restore_method = getattr(cls, restore_method_name)
        return restore_method(data)
    EasyHandler.handles(cls)
    return cls
  return easily_decorated
