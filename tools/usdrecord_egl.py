#!/usr/bin/env python3
#
# Copyright 2019 Pixar
#
# Licensed under the terms set forth in the LICENSE.txt file available at
# https://openusd.org/license.
#

from pxr import Usd
from pxr import UsdGeom, UsdRender
from pxr import Sdf
from pxr import UsdUtils, UsdAppUtils
from pxr import Tf

import argparse
import os
import sys


def _Msg(msg):
    sys.stdout.write(msg + '\n')

def _Err(msg):
    sys.stderr.write(msg + '\n')

def _SetupOpenGLContext(width=100, height=100):
    # PATCHED: Use EGL via ctypes instead of Qt for GL context creation.
    # Enables headless GPU rendering via EGL on systems where Qt's
    # offscreen platform cannot create a GL context.
    import ctypes

    egl = ctypes.cdll.LoadLibrary("libEGL.so.1")
    egl.eglGetDisplay.restype = ctypes.c_void_p
    egl.eglGetDisplay.argtypes = [ctypes.c_void_p]
    egl.eglInitialize.restype = ctypes.c_int
    egl.eglInitialize.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    egl.eglBindAPI.restype = ctypes.c_int
    egl.eglBindAPI.argtypes = [ctypes.c_int]
    egl.eglChooseConfig.restype = ctypes.c_int
    egl.eglChooseConfig.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    egl.eglCreateContext.restype = ctypes.c_void_p
    egl.eglCreateContext.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    egl.eglCreatePbufferSurface.restype = ctypes.c_void_p
    egl.eglCreatePbufferSurface.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    egl.eglMakeCurrent.restype = ctypes.c_int
    egl.eglMakeCurrent.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]

    EGL_DEFAULT_DISPLAY = 0
    EGL_OPENGL_API = 0x30A2
    EGL_OPENGL_BIT = 0x0008
    EGL_RENDERABLE_TYPE = 0x3040
    EGL_SURFACE_TYPE = 0x3033
    EGL_PBUFFER_BIT = 0x0001
    EGL_RED_SIZE = 0x3024
    EGL_GREEN_SIZE = 0x3023
    EGL_BLUE_SIZE = 0x3022
    EGL_DEPTH_SIZE = 0x3025
    EGL_NONE = 0x3038
    EGL_WIDTH = 0x3057
    EGL_HEIGHT = 0x3056

    attrs = (ctypes.c_int * 13)(
        EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
        EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
        EGL_RED_SIZE, 8, EGL_GREEN_SIZE, 8, EGL_BLUE_SIZE, 8,
        EGL_DEPTH_SIZE, 24,
        EGL_NONE
    )

    config = ctypes.c_void_p()
    n = ctypes.c_int()

    dpy = egl.eglGetDisplay(EGL_DEFAULT_DISPLAY)
    if not dpy:
        raise RuntimeError("EGL: no display")
    major, minor = ctypes.c_int(), ctypes.c_int()
    if not egl.eglInitialize(dpy, ctypes.byref(major), ctypes.byref(minor)):
        raise RuntimeError("EGL: initialize failed")
    _Msg("EGL %d.%d" % (major.value, minor.value))
    if not egl.eglBindAPI(EGL_OPENGL_API):
        raise RuntimeError("EGL: bindAPI failed")
    if not egl.eglChooseConfig(dpy, attrs, ctypes.byref(config), 1, ctypes.byref(n)):
        raise RuntimeError("EGL: chooseConfig failed")

    ctx = egl.eglCreateContext(dpy, config, None, None)
    if not ctx:
        raise RuntimeError("EGL: no context")

    pbuf_attrs = (ctypes.c_int * 5)(EGL_WIDTH, width, EGL_HEIGHT, height, EGL_NONE)
    surf = egl.eglCreatePbufferSurface(dpy, config, pbuf_attrs)
    if not surf:
        raise RuntimeError("EGL: no pbuffer")

    if not egl.eglMakeCurrent(dpy, surf, surf, ctx):
        raise RuntimeError("EGL: makeCurrent failed")

    libGL = ctypes.cdll.LoadLibrary("libGL.so.1")
    glXGetProc = libGL.glXGetProcAddressARB
    glXGetProc.restype = ctypes.c_void_p
    glXGetProc.argtypes = [ctypes.c_char_p]
    fp = glXGetProc(b"glGetString")
    if fp:
        glGetString = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_int)(fp)
        raw_version = glGetString(0x1F02)
        raw_renderer = glGetString(0x1F01)
        if raw_version:
            _Msg("GL_VERSION: %s" % raw_version.decode())
        if raw_renderer:
            _Msg("GL_RENDERER: %s" % raw_renderer.decode())

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen") # XXX
    from PySide6.QtWidgets import QApplication
    return QApplication(sys.argv)


def _DumpMallocTags(stage, contextStr):
    if not Tf.MallocTag.IsInitialized():
        _Msg("Unable to accumulate memory usage since the Pxr MallocTag "
            "system was not initialized")
        return

    callTree = Tf.MallocTag.GetCallTree()
    memInMb = Tf.MallocTag.GetTotalBytes() / (1024.0 * 1024.0)

    import os.path as path
    import tempfile
    layerName = path.basename(stage.GetRootLayer().identifier)
    # CallTree.Report() gives us the most informative (and processable)
    # form of output, but it only accepts a fileName argument.  So we
    # use NamedTemporaryFile just to get a filename.
    statsFile = tempfile.NamedTemporaryFile(
        prefix=layerName+'.',
        suffix='.mallocTag',
        delete=False)
    statsFile.close()
    reportName = statsFile.name
    callTree.Report(reportName)
    _Msg("Memory consumption of %s for %s is %d Mb" %
        (contextStr, layerName, memInMb))
    _Msg("For detailed analysis, see " + reportName)

def main() -> int:
    programName = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(prog=programName,
        description='Generates images from a USD file')

    # Positional (required) arguments.
    parser.add_argument('usdFilePath', action='store', type=str,
        help='USD file to record')
    parser.add_argument('outputImagePath', action='store', type=str,
        help=(
            'Output image path. For frame ranges, the path must contain '
            'exactly one frame number placeholder of the form "###" or '
            '"###.###". Note that the number of hash marks is variable in '
            'each group.'))

    # Optional arguments.
    parser.add_argument('--mask', action='store', type=str,
        dest='populationMask', metavar='PRIMPATH[,PRIMPATH...]',
        help=(
            'Limit stage population to these prims, their descendants and '
            'ancestors. To specify multiple paths, either use commas with no '
            'spaces or quote the argument and separate paths by commas and/or '
            'spaces.'))

    parser.add_argument('--purposes', action='store', type=str,
        dest='purposes', metavar='PURPOSE[,PURPOSE...]', default='proxy',
        help=(
            'Specify which UsdGeomImageable purposes should be included '
            'in the renders.  The "default" purpose is automatically included, '
            'so you need specify only the *additional* purposes.  If you want '
            'more than one extra purpose, either use commas with no spaces or '
            'quote the argument and separate purposes by commas and/or spaces.'))

    parser.add_argument('--sessionLayer', action='store', type=str,
        dest='sessionLayerPath', metavar='SESSIONLAYER',
        help=("If specified, the stage will be opened with the "
              "'sessionLayer' in place of the default anonymous layer."))

    # Note: The argument passed via the command line (disableGpu) is inverted
    # from the variable in which it is stored (gpuEnabled).
    parser.add_argument('--disableGpu', action='store_false',
        dest='gpuEnabled',
        help=(
            'Indicates if the GPU should not be used for rendering. If set '
            'this not only restricts renderers to those which only run on '
            'the CPU, but additionally it will prevent any tasks that require '
            'the GPU from being invoked.'))

    # Note: The argument passed via the command line (disableDrawMode) is
    # inverted from the variable in which it is stored (drawModeEnabled).
    parser.add_argument('--disableDrawMode', action='store_false',
        dest='drawModeEnabled',
        help=(
            "Disables support for USD draw modes. If set, UsdGeomModelAPI's "
            'draw modes will be ignored, and no geometry will be replaced '
            'with a draw mode standin. Everything will render as if '
            'applyDrawMode = false.'))

    # Note: The argument passed via the command line (disableCameraLight)
    # is inverted from the variable in which it is stored (cameraLightEnabled)
    parser.add_argument('--disableCameraLight', action='store_false',
        dest='cameraLightEnabled',
        help=(
            'Indicates if the default camera lights should not be used '
            'for rendering.'))

    UsdAppUtils.cameraArgs.AddCmdlineArgs(parser)
    UsdAppUtils.framesArgs.AddCmdlineArgs(parser)
    UsdAppUtils.complexityArgs.AddCmdlineArgs(parser)
    UsdAppUtils.colorArgs.AddCmdlineArgs(parser)
    UsdAppUtils.rendererArgs.AddCmdlineArgs(parser)

    parser.add_argument('--imageWidth', '-w', action='store', type=int,
        default=960,
        help=(
            'Width of the output image. The height will be computed from this '
            'value and the camera\'s aspect ratio (default=%(default)s). '
            'Note that this only affects the command-line output image; '
            'it does not affect any render products in scene description.'))

    parser.add_argument('--enableDomeLightVisibility', action='store_true',
        dest='domeLightVisibility',
        help=('Show the dome light background in the rendered output.  '
            'If this option is not included and there is a dome light in '
            'the stage, the IBL from it will be used for lighting but not '
            'drawn into the background.'))

    parser.add_argument('--renderPassPrimPath', '-rp', action='store', 
        type=str, dest='rpPrimPath', 
        help=(
            'Specify the RenderPass prim to use. This overrides any '
            'renderSettingsPrimPath specified in stage metadata.'))

    parser.add_argument('--renderSettingsPrimPath', '-rs', action='store', 
        type=str, dest='rsPrimPath', 
        help=(
            'Specify the RenderSettings prim to use. This overrides any '
            'renderSettingsPrimPath specified in stage metadata.'))

    parser.add_argument('--traceToFile', action='store',
        type=str, dest='traceToFile', default=None,
        help=(
            'Start tracing at application startup and '
            'write --traceFormat specified format output to the '
            'specified trace file when the application quits'))

    parser.add_argument('--traceFormat', action='store',
        type=str, dest='traceFormat', default='chrome',
        choices=['chrome', 'trace'],
        help=(
            'Output format for trace file specified by '
            '--traceToFile. \'chrome\' files can be read in '
            'chrome, \'trace\' files are simple text reports. '
            '(default=%(default)s)'))

    parser.add_argument('--memstats', action='store_true',
        default=False, dest='memstats',
        help=(
            'Use the Pxr MallocTags memory accounting system to profile '
            'USD, saving results to a tmp file, with a summary to the console. '
            'Will have no effect if MallocTags are not supported in the '
            'USD installation.'))

    args = parser.parse_args()

    args.imageWidth = max(args.imageWidth, 1)

    purposes = args.purposes.replace(',', ' ').split()

    # Track allocations
    if args.memstats:
        Tf.MallocTag.Initialize()

    # Begin tracing
    traceCollector = None
    if args.traceToFile:
        from pxr import Trace
        traceCollector = Trace.Collector()
        traceCollector.enabled = True

    # Load the root layer.
    rootLayer = Sdf.Layer.FindOrOpen(args.usdFilePath)
    if not rootLayer:
        _Err('Could not open layer: %s' % args.usdFilePath)
        return 1

    # Load the session layer.
    if args.sessionLayerPath:
        sessionLayer = Sdf.Layer.FindOrOpen(args.sessionLayerPath)
        if not sessionLayer:
            _Err('Could not open layer: %s' % args.sessionLayerPath)
            return 1
    else:
        sessionLayer = Sdf.Layer.CreateAnonymous()

    # Open the USD stage, using a population mask if paths were given.
    if args.populationMask:
        populationMaskPaths = args.populationMask.replace(',', ' ').split()

        populationMask = Usd.StagePopulationMask()
        for maskPath in populationMaskPaths:
            populationMask.Add(maskPath)

        usdStage = Usd.Stage.OpenMasked(rootLayer, sessionLayer, populationMask)
    else:
        usdStage = Usd.Stage.Open(rootLayer, sessionLayer)

    if not usdStage:
        _Err('Could not open USD stage: %s' % args.usdFilePath)
        return 1

    UsdAppUtils.framesArgs.ValidateCmdlineArgs(parser, args, usdStage,
        frameFormatArgName='outputImagePath')

    # Get the RenderSettings Prim Path.
    # It may be specified directly (--renderSettingsPrimPath),
    # via a render pass (--renderPassPrimPath),
    # or by stage metadata (renderSettingsPrimPath).
    if args.rsPrimPath and args.rpPrimPath:
        _Err('Cannot specify both --renderSettingsPrimPath and '
             '--renderPassPrimPath')
        return 1
    if args.rpPrimPath:
        # A pass was specified, so next we get the associated settings prim.
        renderPass = UsdRender.Pass(usdStage.GetPrimAtPath(args.rpPrimPath))
        if not renderPass:
            _Err('Unknown render pass <{}>'.format(args.rpPrimPath))
            return 1
        sourceRelTargets = renderPass.GetRenderSourceRel().GetTargets()
        if not sourceRelTargets:
            _Err('Render source not authored on {}'.format(args.rpPrimPath))
            return 1
        args.rsPrimPath = sourceRelTargets[0]
        if len(sourceRelTargets) > 1:
            Tf.Warn('Render pass <{}> has multiple targets; using <{}>'.
                format(args.rpPrimPath, args.rsPrimPath))
    if not args.rsPrimPath:
        # Fall back to stage metadata.
        args.rsPrimPath = usdStage.GetMetadata('renderSettingsPrimPath')

    # Get the camera.
    usdCamera = None
    # If a camera was specified directly, use that.
    if args.camera:
        usdCamera = UsdAppUtils.GetCameraAtPath(usdStage, args.camera)
    # If render settings were specified, use the associated camera.
    if not usdCamera and args.rsPrimPath:
        rs = UsdRender.Settings(usdStage.GetPrimAtPath(args.rsPrimPath))
        if rs:
            cameraTargets = rs.GetCameraRel().GetTargets()
            if len(cameraTargets) == 1:
                usdCamera = UsdGeom.Camera(
                    usdStage.GetPrimAtPath(cameraTargets[0]))
    # If no camera has been found, use the pipeline configured default.
    if not usdCamera:
        usdCamera = UsdAppUtils.GetCameraAtPath(usdStage,
            UsdUtils.GetPrimaryCameraName())

    if args.gpuEnabled:
        # UsdAppUtils.FrameRecorder will expect that an OpenGL context has
        # been created and made current if the GPU is enabled.
        #
        # Frame-independent initialization.
        # Note that the size of the widget doesn't actually affect the size of
        # the output image. We just pass it along for cleanliness.
        glWidget = _SetupOpenGLContext(args.imageWidth, args.imageWidth)

    rendererPluginId = UsdAppUtils.rendererArgs.GetPluginIdFromArgument(
        args.rendererPlugin) or ''

    # Initialize FrameRecorder 
    frameRecorder = UsdAppUtils.FrameRecorder(
        rendererPluginId, args.gpuEnabled, args.drawModeEnabled)
    if args.rpPrimPath:
        frameRecorder.SetActiveRenderPassPrimPath(args.rpPrimPath)
    if args.rsPrimPath:
        frameRecorder.SetActiveRenderSettingsPrimPath(args.rsPrimPath)
    frameRecorder.SetImageWidth(args.imageWidth)
    frameRecorder.SetComplexity(args.complexity.value)
    frameRecorder.SetCameraLightEnabled(args.cameraLightEnabled)
    frameRecorder.SetColorCorrectionMode(args.colorCorrectionMode)
    frameRecorder.SetIncludedPurposes(purposes)
    frameRecorder.SetDomeLightVisibility(args.domeLightVisibility)
    frameRecorder.SetPrimaryCameraPrimPath(usdCamera.GetPath())

    _Msg('Camera: %s' % usdCamera.GetPath().pathString)
    _Msg('Renderer plugin: %s' % frameRecorder.GetCurrentRendererId())

    for timeCode in args.frames:
        _Msg('Recording time code: %f' % timeCode)
        outputImagePath = args.outputImagePath.format(frame=timeCode)
        try:
            frameRecorder.Record(usdStage, usdCamera, timeCode, outputImagePath)
        except Tf.ErrorException as e:
            _Err("Recording aborted due to the following failure at time code "
                 "{0}: {1}".format(timeCode, str(e)))
            return 1

    # Release our reference to the frame recorder so it can be deleted before
    # the Qt stuff.
    frameRecorder = None

    # End tracing and report results.
    if traceCollector:
        traceCollector.enabled = False
        if args.traceFormat == 'trace':
            Trace.Reporter.globalReporter.Report(
                args.traceToFile)
        elif args.traceFormat == 'chrome':
            Trace.Reporter.globalReporter.ReportChromeTracingToFile(
                args.traceToFile)
        else:
            Tf.RaiseCodingError("Invalid trace format option provided: %s -"
                    "trace/chrome are the valid options" %
                    args.traceFormat)
    if args.memstats:
        _DumpMallocTags(usdStage, programName)

    return 0


if __name__ == '__main__':
    sys.exit(main())
