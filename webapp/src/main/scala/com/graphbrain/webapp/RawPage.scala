package com.graphbrain.webapp

import unfiltered.request._

import com.graphbrain.db.Vertex
import com.graphbrain.db.UserNode

case class RawPage(vertex: Vertex, user: UserNode, req: HttpRequest[Any], cookies: Map[String, Any]) {
  var html = "<h2>Vertex: " + vertex.id + "</h2>"

  html += vertex.raw

  val edgeIds = WebServer.graph.edges(vertex.id, user.id)
  for (eid <- edgeIds)
    html += eid + "<br />"

  def response = WebServer.scalateResponse("raw.ssp", "raw", vertex.toString, cookies, req, html=html)
}

object RawPage {
}