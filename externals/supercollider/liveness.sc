Liveness {
  classvar  liveness_port;
  var       <>session, <>control_surface, <>responders;

  *initClass {
		//set-up broadcast communication
		NetAddr.broadcastFlag	=	  true;
		liveness_port         =   NetAddr("192.168.1.255", 57121);
  }

	*new {
    arg session = \default, control_surface = \default;
    ^super.new.init(session, control_surface);
  }

  init {
		arg session = \default, control_surface = \default;
    this.session         = session;
    this.control_surface = control_surface;
    this.responders      = Dictionary.new;
  }

  addControl {
    arg type, name, function, initValue = 0;
    var responder, key;

    liveness_port.sendMsg(this.getKey()++"/add_control", type, name, initValue.asString());

    key       = this.getKey()++"/"++name;

    responder = this.responders.at(key);
    if (responder.notNil()) {responder.free;};

    responder = OSCFunc(function, key);
    this.responders.put(key, responder);
  }

  addPreset {
    arg type, name;
    liveness_port.sendMsg(this.getKey()++"/add_preset", name, type);
  }

  getKey {
    ^ ("/" ++ this.session.asString()++ "/" ++ this.control_surface.asString()).stripRTF();
  }
}
