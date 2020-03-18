

CR = 0x0D
LF = 0x0A

SEPARATOR = 0x2C

LEN_SENTENCE_NAME = 3
LEN_CSR = 2


LOG_LEVEL_DEBUG_DEEPER = 9

SEN_BB1 = 'BB1'
SEN_BB2 = 'BB2'
SEN_BC1 = 'BC1'
SEN_BT1 = 'BT1'
SEN_BT2 = 'BT2'
SEN_BT3 = 'BT3'
SEN_BT4 = 'BT4'
SEN_BV1 = 'BV1'
SEN_BV2 = 'BV2'
SEN_CV1 = 'CV1'
SEN_VR1 = 'VR1'

SEN_DT1 = 'DT1'

SEN_ST1 = 'ST1'

SEN_OT1 = 'OT1'

SENTENCES_DEFINITION = {
    SEN_BB1: {'module': 'emus_lib.sentence.bb1', 'class_name': 'BB1'},
    SEN_BB2: {'module': 'emus_lib.sentence.bb2', 'class_name': 'BB2'},

    SEN_BC1: {'module': 'emus_lib.sentence.bc1', 'class_name': 'BC1'},

    SEN_BT1: {'module': 'emus_lib.sentence.bt1', 'class_name': 'BT1'},
    SEN_BT2: {'module': 'emus_lib.sentence.bt2', 'class_name': 'BT2'},
    SEN_BT3: {'module': 'emus_lib.sentence.bt3', 'class_name': 'BT3'},
    SEN_BT4: {'module': 'emus_lib.sentence.bt4', 'class_name': 'BT4'},

    SEN_BV1: {'module': 'emus_lib.sentence.bv1', 'class_name': 'BV1'},
    SEN_BV2: {'module': 'emus_lib.sentence.bv2', 'class_name': 'BV2'},

    SEN_CV1: {'module': 'emus_lib.sentence.cv1', 'class_name': 'CV1'},

    SEN_VR1: {'module': 'emus_lib.sentence.vr1', 'class_name': 'VR1'},

    SEN_DT1: {'module': 'emus_lib.sentence.dt1', 'class_name': 'DT1'},

    SEN_OT1: {'module': 'emus_lib.sentence.ot1', 'class_name': 'OT1'},
}