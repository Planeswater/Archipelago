from ..Rcd import Rcd


class Operation:

    def create(global_flag, operation, value):
        op = Rcd.Operation()
        op.flag = global_flag
        op.operation = operation
        op.op_value = value
        return op
