import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
import onnx_graphsurgeon as gs
from onnx2tf.utils.common_functions import (
    get_constant_or_variable,
    print_node_info,
)


@print_node_info
def make_node(
    *,
    graph_node: gs.Node,
    tf_layers_dict: dict,
    **kwargs: dict,
):
    """Less

    Parameters
    ----------
    graph_node: gs.Node
        graph_surgeon Node

    tf_layers_dict: dict
        optype, shape, dtype, tensorflow graph
    """
    graph_node_input_1 = get_constant_or_variable(graph_node.inputs[0])
    graph_node_input_2 = get_constant_or_variable(graph_node.inputs[1])
    graph_node_output: gs.Variable = graph_node.outputs[0]
    shape = graph_node_output.shape
    dtype = graph_node_output.dtype

    # Preserving Graph Structure (Dict)
    tf_layers_dict[graph_node_output.name] = {
        'optype': graph_node.op,
        'shape': shape,
        'dtype': dtype,
    }

    # Generation of TF OP
    tf_layers_dict[graph_node_output.name]['tf_node'] = \
        tf.math.less(
            x=tf_layers_dict[graph_node_input_1.name]['tf_node'] \
                if isinstance(graph_node_input_1, gs.Variable) else graph_node_input_1,
            y=tf_layers_dict[graph_node_input_2.name]['tf_node'] \
                if isinstance(graph_node_input_2, gs.Variable) else graph_node_input_2,
            name=graph_node.name,
        )
