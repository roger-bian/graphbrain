package com.graphbrain.hgdb


abstract class Textual extends Vertex {
  val summary: String

  // Score edge in terms of its ability to generate a summary for this TextNode
  private def scoreForSummary(edge: Edge): Int = {
    // Only consider edges where this TextNode is the first participant
    if (edge.participantIds(0) != id)
      return -1

    edge.edgeType match {
      case "rtype/1/as_in" => 100
      case "rtype/1/is_a" => 10
      case _ => -1
    }
  }

  def generateSummary: String = {
    val edges = store.neighborEdges(id)

    var bestEdge: Edge = null
    var maxScore = -1
    for (e <- edges) {
      val score = scoreForSummary(e)
      if (score > maxScore) {
        bestEdge = e
        maxScore = score
      }
    }

    if (bestEdge == null)
      ""
    else
      "(" + store.get(bestEdge.participantIds(1)) + ")"
  }

  def updateSummary: Textual = this

  override def description: String = toString + " " + generateSummary
}