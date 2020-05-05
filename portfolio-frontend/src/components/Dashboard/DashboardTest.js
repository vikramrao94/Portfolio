import React, { useEffect, useRef, useState } from "react";
import styled from "styled-components";

const convertTonumber = (percentage, number) =>{
  const result = parseInt(percentage*number/100);
  return result;
}
const DashboardTest = (props) => {
  const defaultState = {};
  const references = useRef(Array.from({length: props.objects.length}, () => React.createRef()));
  props.objects.forEach((item, i) => {
    defaultState[`item${i}`] = false;
  });
  const [show, doShow] = useState(defaultState);
  const [dimensions, setDimensions] = useState({
    height: window.innerHeight,
    width: window.innerWidth
  })

  useEffect(() => {
    const topPos = element => element.getBoundingClientRect().top;
    const divPos = {};
    references.current.forEach((item, i) => {
      divPos[`item${i}`] = topPos(item.current);
    });

    const onScroll = () => {
      const scrollPos = window.scrollY + window.innerHeight;
      for (const [key, value] of Object.entries(divPos)) {
        if(value < scrollPos){
          doShow(state => ({ ...state, [key]: true }));
          break;
        }
      }
    };
    const onResize = () => {
      setDimensions({
        height: window.innerHeight,
        width: window.innerWidth
      });
    };
    window.addEventListener("scroll", onScroll);
    window.addEventListener("resize",onResize);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onResize);
    }
  }, []);
  return (
    <>
      <Wrapper>
        <Header
          width = {convertTonumber(parseInt(props.width),dimensions.width) }
          height = {convertTonumber(parseInt(props.height),dimensions.height) }
          widthMargin = {convertTonumber(((100 - parseInt(props.width)) / 2),dimensions.width)}
          heightMargin = {convertTonumber(((100 - parseInt(props.height)) / 2),dimensions.height)}
        />
        {
          props.objects.map((item,i) => {
            const widthMargin = (100 - parseInt(props.width)) / 2;
            const heightMargin = (100 - parseInt(props.height)) / 2;
            return (
              <Div
                animate = {show[`item${props.objects.length - (i + 1)}`]}
                ref = {references.current[`${props.objects.length - (i + 1)}`]}
                key = {i}
                width = {convertTonumber(parseInt(props.width),dimensions.width) }
                height = {convertTonumber(parseInt(props.height),dimensions.height) }
                widthMargin = {convertTonumber(widthMargin,dimensions.width)}
                heightMargin = {convertTonumber(heightMargin,dimensions.height)}
              >
                {item}
              </Div>
            )
          })
        }

      </Wrapper>
    </>
  );
};

const Header = styled.div`
  height: ${({ height }) => height}px;
  width: ${({ width }) => width}px;
  border-radius: 2em;
  border: 0.1em solid red;
  margin-top: ${({ heightMargin }) => heightMargin}px;
  margin-bottom: ${({ heightMargin }) => heightMargin}px;
  margin-left: ${({ widthMargin }) => widthMargin}px;
  margin-right: ${({ widthMargin }) => widthMargin}px;
`;
const Div = styled.div`
  height: ${({ height }) => height}px;
  width: ${({ width }) => width}px;
  border-radius: 2em;
  border: 0.1em solid red;
  margin-top: ${({ heightMargin }) => heightMargin}px;
  margin-bottom: ${({ heightMargin }) => heightMargin}px;
  margin-left: ${({ widthMargin }) => widthMargin}px;
  margin-right: ${({ widthMargin }) => widthMargin}px;
  visibility: ${({ animate }) => (animate ? "visible" : "hidden")};
  opacity: ${({ animate }) => (animate ? 1 : 0)};
  transition: visibility 0s linear 0.33s, opacity 0.33s linear;
  transition-delay: 0.5s;
`;

const Wrapper = styled.div`
  display: flex;
  flex-flow: column;
`;

export default DashboardTest;
