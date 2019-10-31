


def topological_sort(items):
    provided = set()
    while items:
         remaining_items = []
         emitted = False

         for item, dependencies in items:
             if dependencies.issubset(provided):
                   yield item
                   provided.add(item)
                   emitted = True
             else:
                   remaining_items.append( (item, dependencies) )

         if not emitted:
             raise Exception('sort fail')

         items = remaining_items