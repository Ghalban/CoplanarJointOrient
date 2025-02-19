"""
Coplanar joint orient tool 0.9.0
Ilya Seletsky 2015

TODO (known issues):
-Preview plane size setting (Width and Height)
-Handle when scene is closed while window open to reset things if possible
-Make the preview plane creation somehow not contribute to the undo history if possible or find a different way to
    display a preview plane
-Save settings between runs.
-Fix window not shrinking properly when switching between plane modes.
-Figure out what else crashes

Stretch goals:
-Joint preview.  Preview of how the joints will be oriented in real time without hitting apply button.
-Interactive plane mode.  Move a plane around in real time
-See if I can make UI more intuitive/self documenting and with a bunch of pretty pictures
-Auto compute preview plane size and position based on selected joints.
-Optimize UI change code to prevent unnecessary updates.  Not a real huge issue.
-Redo UI with pyQt to make the UI be more versatile and resizeable and strings localizeable, etc...
"""
import maya.cmds as cmds
import CoplanarJointOrient.mayaUtil
import CoplanarJointOrient.MayaUIValue.VectorValue
import functools


class PositionValue(CoplanarJointOrient.MayaUIValue.VectorValue.VectorValue):
    def __init__(self, label=None, parentUI=None):
        super(PositionValue, self).__init__(label, parentUI)

        if (parentUI is not None):
            cmds.button(self.fromSelectionsButton, edit=True,
                        command=functools.partial(PositionValue.onFromSelectionsPressed, self))

    def onFromSelectionsPressed(self, unused):
        self.computeFromSelections()

    def computeFromNodes(self, nodes):
        self.setValue(CoplanarJointOrient.mayaUtil.getAverageNodePositions(nodes))

    def computeFromSelections(self):
        self.computeFromNodes(cmds.ls(selection=True))
