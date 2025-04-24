from staticfg import CFGBuilder

cfg = CFGBuilder().build_from_file('decision_agent_3.0.py', 'D:/Desktop/xas/FALCON/gjj_decision_agent/decision_agent_3.0.py')

cfg.build_visual('exampleCFG', 'pdf')