from itertools import repeat

from jawa.attribute import Attribute
from jawa.util.verifier import VerificationTypes

# These types are followed by an additional u2.
TYPES_WITH_EXTRA = (
    VerificationTypes.ITEM_Object,
    VerificationTypes.ITEM_Uninitialized
)


class StackMapFrame(object):
    __slots__ = (
        'frame_type',
        'frame_offset',
        'frame_locals',
        'frame_stack'
    )

    def __init__(self, frame_type):
        self.frame_type = frame_type
        self.frame_offset = 0
        self.frame_locals = []
        self.frame_stack = []

    def __repr__(self):
        return (
            u'<StackMapFrame(type={s.frame_type!r},'
            u'offset={s.frame_offset!r},'
            u'locals={s.frame_locals!r},'
            u'stack={s.frame_stack!r})>'
        ).format(s=self)


class StackMapTableAttribute(Attribute):
    """
    .. note::

        Consider this experimental. This is an unnecessary 'feature' added
        in Java6 that even the official JDK has multiple bugs with. Proper
        generation of a StackMapTableAttribute requires a complete class
        hierarchy among other things.
    """
    ADDED_IN = '6.0.0'
    MINIMUM_CLASS_VERSION = (50, 0)

    def __init__(self, table, name_index=None):
        super(StackMapTableAttribute, self).__init__(
            table,
            name_index or table.cf.constants.create_utf8(
                'StackMapTable'
            ).index
        )
        self.frames = []

    def unpack(self, info):
        # Described in "4.7.4. The StackMapTable Attribute"
        length = info.u2()
        # Start with a null-state FULL_FRAME.
        previous_frame = StackMapFrame(255)
        for i in range(length):
            frame_type = info.u1()
            frame = StackMapFrame(frame_type)
            if frame_type < 64:
                # 0 to 63 are SAME_FRAME
                if i == 0:
                    frame.frame_offset = frame_type
                else:
                    frame.frame_offset = previous_frame.frame_offset + \
                            frame_type + 1
                    frame.frame_locals = previous_frame.frame_locals

                self.frames.append(frame)
                previous_frame = frame
                continue
            elif frame_type < 128:
                # 64 to 127 are SAME_LOCALS_1_STACK_ITEM
                if i == 0:
                    frame.frame_offset = frame_type - 64
                else:
                    frame.frame_offset = previous_frame.frame_offset + \
                            frame_type - 63
                    frame.frame_locals = previous_frame.frame_locals

                frame.frame_stack = list(
                    self._unpack_verification_type_info(info, 1)
                )

                self.frames.append(frame)
                previous_frame = frame
                continue
            elif frame_type < 247:
                # Reserved types, we may be trying to parse a ClassFile that's
                # newer than we can handle.
                raise NotImplementedError()

            # All other types have an additional offset
            frame_offset = info.u2()

            if frame_type == 247:
                # SAME_LOCALS_1_STACK_ITEM_EXTENDED
                if i == 0:
                    frame.frame_offset = frame_offset
                else:
                    frame.frame_offset = previous_frame.frame_offset + \
                            frame_offset + 1
                frame.frame_locals = previous_frame.frame_locals
                frame.frame_stack = list(
                    self._unpack_verification_type_info(
                        info,
                        1
                    )
                )
            elif frame_type < 251:
                # CHOP
                if i == 0:
                    frame.frame_offset = frame_offset
                else:
                    frame.frame_offset = previous_frame.frame_offset + \
                            frame_offset + 1
                    frame.frame_locals = previous_frame.frame_locals[
                        0:251 - frame_type
                    ]
            elif frame_type == 251:
                # SAME_FRAME_EXTENDED
                if i == 0:
                    frame.frame_offset = frame_offset
                else:
                    frame.frame_offset = previous_frame.frame_offset + \
                            frame_offset + 1
                    frame.frame_locals = previous_frame.frame_locals
            elif frame_type < 255:
                # APPEND
                if i == 0:
                    frame.frame_offset = frame_offset
                else:
                    frame.frame_offset = previous_frame.frame_offset + \
                            frame_offset + 1

                frame.frame_locals = previous_frame.frame_locals + list(
                    self._unpack_verification_type_info(
                        info,
                        frame_type - 251
                    )
                )
            elif frame_type == 255:
                # FULL_FRAME
                if i == 0:
                    frame.frame_offset = frame_offset
                else:
                    frame.frame_offset = previous_frame.frame_offset + \
                            frame_offset + 1

                frame.frame_locals = list(self._unpack_verification_type_info(
                    info,
                    info.u2()
                ))
                frame.frame_stack = list(self._unpack_verification_type_info(
                    info,
                    info.u2()
                ))

            self.frames.append(frame)
            previous_frame = frame

    @staticmethod
    def _unpack_verification_type_info(info, count):
        # Unpacks the verification_type_info structure, used for both locals
        # and the stack.
        for _ in repeat(None, count):
            tag = info.u1()
            if tag in TYPES_WITH_EXTRA:
                yield (tag, info.u2())
            else:
                yield (tag,)

    def pack(self):
        raise NotImplementedError()
