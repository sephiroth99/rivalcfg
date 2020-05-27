import sys
import argparse

from . import cli
from . import devices
from . import get_first_mouse


def main(args):
    mouse = get_first_mouse()

    cli_parser = argparse.ArgumentParser(prog="rivalcfg")
    cli.add_main_cli(cli_parser)

    if mouse:
        mouse_profile = devices.get_profile(
                vendor_id=mouse.vendor_id,
                product_id=mouse.product_id)
        cli.add_mouse_cli(cli_parser, mouse_profile)

    settings = cli_parser.parse_args(args)

    # Reset
    if mouse and settings.RESET:
        mouse.reset_settings()

    # Apply settings
    if mouse:
        for setting_name, value in [
                (k.lower(), v) for k, v in vars(settings).items()]:
            if value is None:
                continue
            method_name = "set_%s" % setting_name
            if not hasattr(mouse, method_name):
                continue
            getattr(mouse, method_name)(value)

        # Save settings in the internal device memory
        if settings.SAVE:
            mouse.save()


if __name__ == "__main__":
    main(sys.argv[1:])
