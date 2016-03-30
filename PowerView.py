import sublime, sublime_plugin
import bisect, copy

global powerView;

START_COLUMN = 0
START_ROW = 1
END_COLUMN = 2
END_ROW = 3

class PowerView:

    padding = 0.01
    storedLayouts = {}

    def zoom_cell_in(self, groupNum):
        window = sublime.active_window()
        groupNum = window.active_group()
        layout = window.get_layout()

        newRows = self.move_inside_edge(layout['cells'][groupNum][START_ROW], -0.1, layout['rows'])
        newRows = self.move_outside_edge(layout['cells'][groupNum][END_ROW], 0.1, newRows)
        layout["rows"] = newRows

        newCols = self.move_inside_edge(layout['cells'][groupNum][START_COLUMN], -0.1, layout['cols'])
        newCols = self.move_outside_edge(layout['cells'][groupNum][END_COLUMN], 0.1, newCols)
        layout["cols"] = newCols

        sublime.active_window().set_layout(layout)
        window.focus_group(groupNum)

    def zoom_cell_out(self, groupNum):
        window = sublime.active_window()
        groupNum = window.active_group()
        layout = window.get_layout()

        newRows = self.move_inside_edge(layout['cells'][groupNum][START_ROW], 0.1, layout['rows'])
        newRows = self.move_outside_edge(layout['cells'][groupNum][END_ROW], -0.1, newRows)
        layout["rows"] = newRows

        newCols = self.move_inside_edge(layout['cells'][groupNum][START_COLUMN], 0.1, layout['cols'])
        newCols = self.move_outside_edge(layout['cells'][groupNum][END_COLUMN], -0.1, newCols)
        layout["cols"] = newCols

        sublime.active_window().set_layout(layout)
        window.focus_group(groupNum)


    def move_outside_edge(self, index, growth, group):

        # return if outside edge is outer most edge
        if (group[index] == 1):
            return group

        # new array of locations after moves
        newGroup = list(group)

        # make sure index is within the padding
        newLocation = group[index] + growth
        maxLocation = 1 - (((len(group)-index) - 1) * self.padding)
        minLocation = (newGroup[index-1]) + self.padding
        if (newLocation > maxLocation):
            newLocation = maxLocation

        if (newLocation < minLocation):
            newLocation = minLocation

        # no changes where made.
        if (newGroup[index] == newLocation):
            return newGroup;

        newGroup[index] = newLocation

        # existing distance of outer edge to outer most edge
        oldSpace = 1 - group[index]
        # new distance of outer edge to outer most edge
        newSpace = 1 - newGroup[index]

        for i in range(index+1, len(group)-1):
            oldDist = group[i] - group[i-1]
            newDist = (oldDist / oldSpace) * newSpace
            if (newDist < (self.padding * 1.25)):
                newDist = self.padding

            newLocation = newGroup[i-1] + newDist
            maxLocation = 1 - (((len(group) - i) - 1) * self.padding)

            if (newLocation > maxLocation):
                newLocation = maxLocation

            newGroup[i] = newLocation
            pass

        return newGroup


    def move_inside_edge(self, index, growth, group):

        # return if outside edge is outer most edge
        if (group[index] == 0):
            return group

        # new array of locations after moves
        newGroup = list(group)

        # make sure index is within the padding
        newLocation = group[index] + growth
        maxLocation = 1 - (((len(group)-index) - 1) * self.padding)
        minLocation = (newGroup[index-1]) + self.padding

        if (newLocation > maxLocation):
            newLocation = maxLocation

        if (newLocation < minLocation):
            newLocation = minLocation

        # no changes where made.
        if (newGroup[index] == newLocation):
            return newGroup;

        newGroup[index] = newLocation

        # existing distance of outer edge to outer most edge
        oldSpace = group[index]
        # new distance of outer edge to outer most edge
        newSpace = newGroup[index]


        for i in range(index-1, 0, -1):
            oldDist = group[i+1] - group[i]
            newDist = (oldDist / oldSpace) * newSpace

            if (newDist < (self.padding * 1.25)):
                newDist = self.padding

            newLocation = newGroup[i+1] - newDist
            minLocation = (newGroup[i-1]) + self.padding

            if (newLocation < minLocation):
                newLocation = minLocation

            newGroup[i] = newLocation
            pass

        return newGroup

    def mega_zoom(self):
        window = sublime.active_window()
        groupNum = window.active_group()

        if (window.id() in self.storedLayouts):
            layout = self.storedLayouts[window.id()]
            del self.storedLayouts[window.id()]

        else:
            layout = window.get_layout()
            self.storedLayouts[window.id()] = copy.deepcopy(layout)

            newRows = self.move_inside_edge_max(layout['cells'][groupNum][START_ROW], layout['rows'])
            newRows = self.move_outside_edge_max(layout['cells'][groupNum][END_ROW], newRows)
            layout["rows"] = newRows

            newCols = self.move_inside_edge_max(layout['cells'][groupNum][START_COLUMN], layout['cols'])
            newCols = self.move_outside_edge_max(layout['cells'][groupNum][END_COLUMN], newCols)
            layout["cols"] = newCols

        sublime.active_window().set_layout(layout)
        window.focus_group(groupNum)


    def move_outside_edge_max(self, index, group):
        newGroup = list(group)
        for i in range(index, len(group)):
            newGroup[i] = 1
            pass
        return newGroup
        pass
    def move_inside_edge_max(self, index, group):
        newGroup = list(group)
        for i in range(index, 0, -1):
            newGroup[i] = 0
            pass
        return newGroup
        pass

    def restore_stored_layout(self):
        window = sublime.active_window()
        groupNum = window.active_group()
        sublime.active_window().set_layout(self.storedLayout)
        window.focus_group(groupNum)



class PowerViewTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        global powerView
        powerView.mega_zoom()
        pass

class PowerViewMegaZoomCommand(sublime_plugin.WindowCommand):
    def run(self):
        global powerView
        powerView.mega_zoom()
        pass

class PowerViewZoomInCommand(sublime_plugin.WindowCommand):
    def run(self):
        global powerView
        groupNum = self.window.active_group()
        powerView.zoom_cell_in(groupNum)
        pass

class PowerViewZoomOutCommand(sublime_plugin.WindowCommand):
    def run(self):
        global powerView
        groupNum = self.window.active_group()
        powerView.zoom_cell_out(groupNum)
        pass

powerView = PowerView()
