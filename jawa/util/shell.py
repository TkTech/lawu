import code

try:
    from IPython.terminal import embed
except ImportError:
    IPYTHON_SHELL_AVAILABLE = False
    embed = None
else:
    IPYTHON_SHELL_AVAILABLE = True


def start_shell(local_ns=None):
    """Create and immediately drop into a Python shell.

    If IPython version 5 or greater is available it will be used instead
    of the built-in python shell.

    :params local_ns: An optional dict containing the global namespace of
                       the newly created shell.
    :type local_ns: dict
    """
    if IPYTHON_SHELL_AVAILABLE:
        # Don't try to stop IPython from displaying its banner, since
        # it's different in every major version
        terminal = embed.InteractiveShellEmbed(user_ns={})
        terminal.mainloop(local_ns=local_ns, global_ns={})
    else:
        code.interact(banner='', local=local_ns)
