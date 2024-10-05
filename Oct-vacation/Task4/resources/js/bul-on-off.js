function changeImage() {
  // TODO
  // 在此处，实现小灯开关的功能！
  element=document.getElementById('myimage')
	if (element.src.match("bulbon"))
	{
		element.src="/imgs/pic_bulboff.gif";
	}
	else
	{
		element.src="/imgs/pic_bulbon.gif";
	}
}
