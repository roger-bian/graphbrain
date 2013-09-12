package com.graphbrain.eco.nodes

import com.graphbrain.eco.{NodeType, Prog}

class NumberNode(prog: Prog, val value: Double) extends ProgNode(prog) {
  override def eval(): AnyVal = value

  def ntype = NodeType.Number
}